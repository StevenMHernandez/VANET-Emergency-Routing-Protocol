"""Contains data structures for the vehicle network."""

__author__ = 'Adam Morrissett'

import csv

from vanet_sim import road_net


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

        self.prev_time = 0
        self.congestion_detected = False

    def update(self, time):
        """Updates state of vehicle with respect to current time."""

        self._update_pos(time)
        print(f't = {time}, v{self.id}: on {self.cur_road.name}, {self.cur_pos}')

    def _update_pos(self, time):
        """Updates position of vehicle with respect to current time."""

        d_pos = (time - self.prev_time) * self.spd

        if self.cur_pos + d_pos >= self.cur_road.length:
            d_pos -= self.cur_road.length
            self._next_road()

        self.cur_pos += d_pos

        if self.cur_pos <= road_net.INTERSECTION_RADIUS:
            self.at_intersection = True
        else:
            self.at_intersection = True

        self.prev_time = time

    def _next_road(self):
        """Moves vehicle to next road in route.

        Vehicle is restarted at the beginning of the route if it is
        currently at the end of the list.
        """

        self.route_index = (self.route_index + 1) % len(self.route)
        self.cur_road = self.route[self.route_index]


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
