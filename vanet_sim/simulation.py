"""Contains code to run the simulations."""
import os
import time

__author__ = 'Adam Morrissett', 'Steven M. Hernandez'

from vanet_sim.evaluation import Evaluations
from vanet_sim.routing.routing_protocols import UrbanRoutingProtocol, Epidemic

LOG_TO_FILE = True
URBAN_ROUTING_STRING = "urban"
EPIDEMIC_ROUTING_STRING = "epidemic"


class Simulation:
    """Performs a simulation."""

    def __init__(self, d_time, road_map, vehicle_net):
        """Custom constructor that initializes parameters.

        :param d_time: simulation time resolution
        :param road_map: filepath of the road network config file
        :param vehicle_net: filepath of the vehicle network config file
        """
        self.cur_time = 0
        self.d_time = d_time
        self.road_net = road_map
        self.vehicle_net = vehicle_net

        self.experiment_storage = "../storage/experiments/{}/".format(time.time())
        os.makedirs(self.experiment_storage)

        self.settings = {
            "communication_radius": 75,
            "protocol": {
                "type": URBAN_ROUTING_STRING,
                # "type": EPIDEMIC_ROUTING_STRING,
                "max_hops": 5,
                "forwarder_ttl": 5,
            }
        }

        self.write_settings_to_file()

    def step(self):
        """Progresses the simulation forward by one time derivative."""

        # Update vehicle locations first
        for vehicle in self.vehicle_net:
            vehicle.update_location(self.cur_time)

        # Collect list of neighbors
        for vehicle in self.vehicle_net:
            vehicle.update_neighbors(self.vehicle_net, self.settings["communication_radius"])

        # Update the routing state
        for v in self.vehicle_net:
            v.update_routing(self.cur_time)

        # Find the current forwarders
        current_forwarders = []
        for vehicle in self.vehicle_net:
            if vehicle.is_current_forwarder:
                current_forwarders.append(vehicle)

        # Route the message from the current forwarder
        for f_curr in current_forwarders:
            protocols = {
                URBAN_ROUTING_STRING: UrbanRoutingProtocol,
                EPIDEMIC_ROUTING_STRING: Epidemic,
            }
            protocol = protocols[self.settings["protocol"]["type"]]
            protocol.route_message(protocol, f_curr, self.settings["protocol"], self.vehicle_net, self.cur_time)

        print(Evaluations.run(self.cur_time, self.vehicle_net))

        if LOG_TO_FILE:
            Evaluations.write_to(self.experiment_storage, self.cur_time, self.vehicle_net)

        self.cur_time += self.d_time

    def run(self, time_duration):
        """Executes the simulation for the specified duration.

        This is on top of previous simulation time.
        """

        print(f'Starting simulation from t = {self.cur_time:.3f}')

        while self.cur_time < time_duration:
            self.step()

    def write_settings_to_file(self):
        if LOG_TO_FILE:
            f = open(self.experiment_storage + "settings.txt", 'w')
            f.write("\n".join(map(lambda x: '"{}": {}'.format(x, self.settings[x]), self.settings)))
            f.close()
