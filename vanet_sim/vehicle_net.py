"""Contains data structures for the vehicle network."""

__author__ = 'Adam Morrissett', 'Steven M. Hernandez'

import csv
import math

from vanet_sim import road_net

COMMUNICATION_RADIUS = 125


class Vehicle:
    def __init__(self, node_id, route):
        """Custom constructor for Vehicle.

        :param node_id: ID number of vehicle
        :param route: list of Roads on which the vehicle travels
        """

        self.id = node_id
        self.route = route

        self.route_index = 0
        self.cur_road = self.route[self.route_index]
        self.spd = self.cur_road.spd_lim
        self.cur_pos = 0
        self.at_intersection = False
        self.is_current_forwarder = False

        self.x = 0
        self.y = 0
        self.prev_time = 0
        self.neighbors = []

        self.congestion_detected = False

        self.affected_at = None
        self.received_at = None

        self.update_location(0)

    def update_location(self, time):
        """Updates position of vehicle with respect to current time.

        Each vehicle has 2 positions: relative to intersections and
        absolute with respect to the map.

        :param time: current simulation time
        :return: None
        """

        d_pos = (time - self.prev_time) * self.spd
        fwd_n = self._get_forward_neighbor()

        if fwd_n is not None and d_pos > _calc_distance(self, fwd_n) - 16:
            d_pos = _calc_distance(self, fwd_n) - 16

            if self.cur_road.is_obstructed:
                self.spd = 0
                self.affected_at = time

        elif (self.cur_road.is_obstructed
                and self.cur_pos + d_pos >= self.cur_road.obstruction_pos):
            d_pos = 0
            self.spd = 0.0
            self.affected_at = time
        elif self.cur_pos + d_pos >= self.cur_road.length:
            d_pos -= self.cur_road.length
            self._next_road()

        self.cur_pos += d_pos

        self.at_intersection = self.cur_pos <= road_net.INTERSECTION_RADIUS

        # Absolute positioning helps for determining neighbors and
        # placement on GUI.
        x_range = self.cur_road.end_node.x_pos - self.cur_road.start_node.x_pos
        y_range = self.cur_road.end_node.y_pos - self.cur_road.start_node.y_pos

        self.x = (self.cur_road.start_node.x_pos
                  + (x_range * self.cur_pos / self.cur_road.length))
        self.y = (self.cur_road.start_node.y_pos
                  + (y_range * self.cur_pos / self.cur_road.length))

        self.prev_time = time

    def _next_road(self):
        """Moves vehicle to next road in route.

        Vehicle is restarted at the beginning of the route if it is
        currently at the end of the route list.

        :return: None
        """

        self.route_index = (self.route_index + 1) % len(self.route)
        self.cur_road = self.route[self.route_index]
        self.spd = self.cur_road.spd_lim

    def _get_forward_neighbor(self):
        """Gets the vehicle in front of itself.

        :return: Vehicle in front of itself
        """

        for n in self.neighbors:
            if n.cur_road == self.cur_road and n.cur_pos > self.cur_pos:
                return n

    def update_neighbors(self, vehicle_net):
        """ Updates the list of neighbors that the vehicle sees.

        :param vehicle_net: the vehicle network
        :return: None
        """

        self.neighbors = []

        for v in vehicle_net:
            if (v.id != self.id
                    and _calc_distance(self, v) < COMMUNICATION_RADIUS):
                self.neighbors.append(v)

    def update_routing(self, time):
        # If a vehicle becomes obstructed without receiving warning,
        # it becomes the current forwarder. We might consider
        # different logic here. Should only one current forwarder be
        # allowed for example.
        if self.affected_at == time and self.received_at is None:
            self.is_current_forwarder = True


def build_vehicle_net(filepath, road_map):
    """Builds a List of Vehicle object from file.

    :param filepath: path to file
    :param road_map: graph of the road network
    :return List of Vehicle objects
    """

    ret_list = []

    with open(file=filepath, mode='r', newline='') as fp:
        reader = csv.reader(fp, delimiter=';')

        for row in reader:
            route = []

            for road in row[1].split(','):
                route.append(road_map.road_dict[road])

            ret_list.append(Vehicle(node_id=int(row[0]), route=route))

    return ret_list


def _calc_distance(v0, v1):
    """Calculates the distance between two vehicles.

    :param v0: first vehicle
    :param v1: second vehicle
    :return: the Euclidean distance between vehicles
    """

    return math.sqrt((v1.x - v0.x) ** 2 + (v1.y - v0.y) ** 2)
