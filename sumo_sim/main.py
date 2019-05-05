import math
import xml.etree.ElementTree as ET

from sumo_sim.evaluation import Evaluations
from sumo_sim.routing.GyTar import GyTar
from sumo_sim.routing.UrbanRoutingIntersection import UrbanRoutingIntersection
from sumo_sim.routing.Epidemic import Epidemic
from sumo_sim.routing.Message import Message
from sumo_sim.routing.UrbanRoutingHops import UrbanRoutingHops
from sumo_sim.routing.InterestedOnlyProtocol import InterestedOnlyProtocol

#
# Collect data from XML first,
# Then delete references to XML so that data is not polled per loop
#
sumocfg = ET.parse('sumo/grid.sumocfg').getroot()
net = ET.parse('sumo/grid.net.xml').getroot()
rou = ET.parse('sumo/grid.rou.xml').getroot()
bt = ET.parse('storage/sumo/grid.bt.out.xml').getroot()
vehroute = ET.parse('storage/sumo/grid.vehroute.out.xml').getroot()
fcd = ET.parse('storage/sumo/grid.fcd.out.xml').getroot()

# Collect data initially first instead of during the simulation loops!
begin = int(sumocfg.find('time/begin').get('value'))
end = int(sumocfg.find('time/end').get('value'))
junctions = {j.get('id'): (float(j.get('x')), float(j.get('y'))) for j in net.findall("junction")}
to_and_from_for_edge = {e.get("id"): (e.get("from"), e.get("to")) for e in net.findall("edge") if not e.get("function")}
vehicles_per_time_step = [[y.get("id") for y in x.findall("vehicle")] for x in fcd.findall("timestep")]
vehicle_location_per_time_step = [
    {y.get("id"): (float(y.get("x")), float(y.get("x")), y.get("lane")) for y in x.findall("vehicle")} for x in
    fcd.findall("timestep")]
vehicle_routes = {x.get("id"): x.find("route").get("edges").split(" ") for x in rou.findall("vehicle")}
vehicles_left_road_at = {x.get("id"): [float(y) for y in x.find("route").get("exitTimes").split(" ") if y] for x in
                         vehroute.findall("vehicle")}

vehicle_ids = [x.get('id') for x in vehroute.findall('vehicle')]
vaporized_vehicle_ids = [x.get('id') for x in vehroute.findall('vehicle') if not x.get('arrival')]
num_vehicles = len(vehicle_ids)

# Determine the last time a given vehicle was moving (e.g. when it was first queued)
last_time_moving = {}
last_road_moving_on = {}
for i in vehicle_ids:
    last_time_moving[i] = 0
for x in fcd.findall('timestep'):
    for y in x.findall('vehicle'):
        if float(y.get('speed')):
            last_time_moving[y.get('id')] = float(x.get('time'))
            last_road_moving_on[y.get('id')] = y.get('lane').split("_")[0]
last_time_moving = {k: v for k, v in last_time_moving.items() if k in vaporized_vehicle_ids}
last_road_moving_on = {k: v for k, v in last_road_moving_on.items() if k in vaporized_vehicle_ids}


# sumocfg = None
# net = None
# bt = None
# vehroute = None
# fcd = None


class SUMOVehicle:
    def __init__(self, id, route, left_road_at, last_road_moving_on):
        self.id = id
        self.received_at = None
        self.affected_at = None
        self.is_current_forwarder = False
        self.original_forwarder = None
        self._msg = None
        self.exists = False
        self.x = None
        self.y = None
        self.lane = None
        self.edge = None
        self.roads = route
        self.left_road_at = left_road_at
        self.last_intersection = None
        self.cur_road = None
        self.started_at = None
        self.last_road_moving_on = last_road_moving_on
        self.received_before_incident_road = None

    @property
    def passed_previous_intersection_at(self):
        i = self.roads.index(self.cur_road)
        if i == 0:
            return self.started_at
        return self.left_road_at[i - 1]

    @property
    def is_on_an_incident_road(self):
        return self.last_road_moving_on is not None and self.last_road_moving_on == self.cur_road

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        if self._msg is None:
            self.received_before_incident_road = not self.is_on_an_incident_road
            self._msg = msg

    def route_contains_rd(self, settings, road):
        i = self.roads.index(self.cur_road)
        r = (max(0, i - settings["num_previous_roads"]), min(len(self.roads), i + settings["num_future_roads"]))
        return road in self.roads[r[0]:r[1]]


vehicles = {i: SUMOVehicle(i, vehicle_routes[i.split(".")[0]],
                           vehicles_left_road_at[i],
                           last_road_moving_on[i] if i in last_road_moving_on else None)
            for i in vehicle_ids}

URBAN_ROUTING_INT_STRING = "urban-int"
URBAN_ROUTING_HOPS_STRING = "urban-hops"
EPIDEMIC_ROUTING_STRING = "epidemic"
GYTAR_ROUTING_STRING = "gytar"
INTERESTED_ONLY_ROUTING_STRING = "interested-only"

settings = {
    "intersection_radius": 25,
    "communication_radius": 45,
    "protocol": {
        # "type": URBAN_ROUTING_INT_STRING,
        # "type": URBAN_ROUTING_HOPS_STRING,
        # "type": EPIDEMIC_ROUTING_STRING,
        # "type": GYTAR_ROUTING_STRING,
        "type": INTERESTED_ONLY_ROUTING_STRING,
        "max_hops": 5,
        "max_ints": 1,
        "min_feed_ratio": 0.1,
        "forwarder_ttl": 5,
        "num_previous_roads": 10,
        "num_future_roads": 10,
    }
}


def distance(vehicle, junction):
    return math.sqrt(pow(vehicle.x - junction[0], 2) + pow(vehicle.y - junction[1], 2))


# for t in range(begin, end):
for t in range(len(vehicles_per_time_step)):
    # Determine which vehicles exist at this time
    # Update their internal state
    for i in vehicles:
        if i in vehicles_per_time_step[t]:
            if not vehicles[i].exists:
                vehicles[i].started_at = t
            vehicles[i].exists = True
            vehicles[i].x = vehicle_location_per_time_step[t][i][0]
            vehicles[i].y = vehicle_location_per_time_step[t][i][1]
            vehicles[i].lane = vehicle_location_per_time_step[t][i][2]
            vehicles[i].edge = vehicles[i].lane.split("_")[0]
            vehicles[i].cur_road = vehicles[i].edge
        else:
            vehicles[i].exists = False

    # For all vehicles which were stopped by the traffic event:
    for i in vaporized_vehicle_ids:
        if vehicles[i].exists:
            # Determine if vehicle is at an intersection
            if vehicles[i].edge in to_and_from_for_edge:
                (j_to, j_from) = to_and_from_for_edge[vehicles[i].edge]
                junctions_to_search = [junctions[j_to], junctions[j_from]]
            else:
                junctions_to_search = [junctions[vehicles[i].lane]]

            vehicles[i].at_intersection = len(
                [1 for j in junctions_to_search if distance(vehicles[i], j) < settings["intersection_radius"]])

            # If vehicle is stopped @time=t
            if t == last_time_moving[i]:
                vehicles[i].affected_at = t
                # if vehicle was not notified in the past
                if vehicles[i].affected_at == t:
                    # vehicle becomes current forwarder
                    vehicles[i].is_current_forwarder = True
                    src_rd = vehicles[i].lane.split("_")[0]
                    vehicles[i].msg = Message(src_rd=src_rd, dst_isect=to_and_from_for_edge[src_rd][0])

    current_forwarders = [j for j in vehicles if vehicles[j].is_current_forwarder]
    # For each current forwarder:
    for i in current_forwarders:
        # Determine current neighbors
        neighbors = [vehicles[s.get('id')] for s in bt.find("bt[@id='" + str(i) + "']").findall("seen") if
                     float(s.get("tBeg")) < t < float(s.get("tEnd"))]
        # routing protocol
        protocols = {
            URBAN_ROUTING_HOPS_STRING: UrbanRoutingHops,
            URBAN_ROUTING_INT_STRING: UrbanRoutingIntersection,
            EPIDEMIC_ROUTING_STRING: Epidemic,
            GYTAR_ROUTING_STRING: GyTar,
            INTERESTED_ONLY_ROUTING_STRING: InterestedOnlyProtocol,
        }
        protocol = protocols[settings["protocol"]["type"]]()
        remains_forwarder = protocol.route_message(vehicles[i], settings['protocol'], vehicles, neighbors, t,
                                                   to_and_from_for_edge)
        vehicles[i].is_current_forwarder = remains_forwarder

    print(Evaluations.run(t, [v for i, v in vehicles.items()]))

neighbors_per_vehicle_per_time = []
