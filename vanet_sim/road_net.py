"""Contains data structures for the road network."""


__author__ = 'Adam Morrissett'


import csv
import math


INTERSECTION_RADIUS = 5


class RoadMap:
    def __init__(self, intersection_file, road_file):
        self.int_dict = RoadMap._build_intersection_grid(intersection_file)
        self.road_dict = RoadMap._build_road_net(road_file, self.int_dict)

    @staticmethod
    def _build_intersection_grid(filepath):
        """Builds an intersection dictionary from CSV file.

        :param filepath: path to file
        :return: dict object
        """

        ret_dict = {}

        with open(file=filepath, mode='r', newline='') as fp:
            reader = csv.reader(fp, delimiter=',')

            for row in reader:
                ret_dict[row[0]] = Intersection(name=row[0],
                                                x_pos=float(row[1]),
                                                y_pos=float(row[2]))

        return ret_dict

    @staticmethod
    def _build_road_net(filepath, intersections):
        """Builds an RoadNet object from file-based specifications.

        :param filepath: path to file
        :return: RoadNet object
        """

        ret_dict = {}

        with open(file=filepath, mode='r', newline='') as fp:
            reader = csv.reader(fp, delimiter=',')

            for row in reader:
                road_name = "{}{}".format(row[0], row[1])
                start_int = intersections[row[0]]
                end_int = intersections[row[1]]
                length = RoadMap._calc_dist(start_int, end_int)

                ret_dict[road_name] = Road(name=road_name,
                                           start_node=start_int,
                                           end_node=end_int,
                                           length=length,
                                           spd_lim=float(row[2]),
                                           is_obstructed=bool(int(row[3])))

        return ret_dict

    @staticmethod
    def _calc_dist(start, end):
        return math.sqrt(pow((end.x_pos - start.x_pos), 2)
                         + pow((end.y_pos - start.y_pos), 2))


class Road:
    """Plain old data (POD) object for a road segment."""

    def __init__(self, name, start_node, end_node, length, spd_lim,
                 is_obstructed):
        """Custom constructor for Road object.

        :param name: name of the road
        :param start_node: intersection at road start
        :param end_node: intersection at road end
        :param length: length of road
        :param spd_lim: speed limit on road
        :param is_obstructed: whether or not road is obstructed
        """
        self.name = name
        self.start_node = start_node
        self.end_node = end_node
        self.length = length
        self.spd_lim = spd_lim
        self.is_obstructed = is_obstructed


class Intersection:
    """Plain old data (POD) object for an intersection."""

    def __init__(self, name, x_pos, y_pos):
        """Custom constructor for Intersection object.

        :param name:
        :param x_pos:
        :param y_pos:
        """
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
