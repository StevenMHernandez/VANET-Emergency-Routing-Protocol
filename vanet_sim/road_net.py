"""Contains data structures for the road network."""

__author__ = 'Adam Morrissett'

import csv

INTERSECTION_RADIUS = 5


class RoadMap:
    def __init__(self):
        pass


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


def build_road_map(filepath):
    """Builds an RoadNet object from file-based specifications.

    :param filepath: path to file
    :return: RoadNet object
    """

    ret_dict = {}

    with open(file=filepath, mode='r', newline='') as fp:
        reader = csv.reader(fp, delimiter=',')

        for row in reader:
            road_name = "{}{}".format(row[0], row[1])
            ret_dict[road_name] = Road(name=road_name,
                                       start_node=row[0],
                                       end_node=row[1],
                                       length=float(row[2]),
                                       spd_lim=float(row[3]),
                                       is_obstructed=bool(row[4]))

    return ret_dict
