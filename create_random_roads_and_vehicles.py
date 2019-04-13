"""Create random roads and vehicles which would not be possible by hand.

"""
import math
import random

__author__ = 'Adam Morrissett', 'Steven M. Hernandez'

NUM_INTERSECTIONS_X = 9
NUM_INTERSECTIONS_Y = 14
NUM_VEHICLES = 100
NUM_INTERSECTIONS_PER_VEHICLE = 20
OBSTRUCTION_START = (5, 2)
OBSTRUCTION_END = (6, 2)

open('intersections.generated.csv', 'w').close()
open('roads.generated.csv', 'w').close()
open('vehicles.generated.csv', 'w').close()

#
# Create intersections file
#
f = open('intersections.generated.csv', 'a')
for intersections_x in range(0, NUM_INTERSECTIONS_X):
    for intersections_y in range(0, NUM_INTERSECTIONS_Y):
        f.write("i{}{},{},{}\n".format(intersections_x, intersections_y, intersections_y * 100, intersections_x * 100))
f.close()


def write_both_ways(x_0, y_0, x_1, y_1):
    obstruction = (OBSTRUCTION_START[0] == x_0 and OBSTRUCTION_START[1] == y_0 and
                   OBSTRUCTION_END[0] == x_1 and OBSTRUCTION_END[1] == y_1)
    obstruction = 1 if obstruction else 0
    int_0 = "i{}{}".format(x_0, y_0)
    int_1 = "i{}{}".format(x_1, y_1)
    spd = math.ceil(random.random() * 10) + 5
    f.write("{},{},{},{}\n".format(int_0, int_1, spd, obstruction))
    f.write("{},{},{},{}\n".format(int_1, int_0, spd, obstruction))


#
# Create roads file
#
f = open('roads.generated.csv', 'a')
for intersections_x in range(0, NUM_INTERSECTIONS_X):
    for intersections_y in range(0, NUM_INTERSECTIONS_Y):
        # BELOW
        if intersections_y < NUM_INTERSECTIONS_Y - 1:
            write_both_ways(intersections_x, intersections_y, intersections_x, intersections_y + 1)

        # RIGHT
        if intersections_x < NUM_INTERSECTIONS_X - 1:
            write_both_ways(intersections_x, intersections_y, intersections_x + 1, intersections_y)

f.close()


#
# Create vehicles
#
def random_ternary():
    """
    Returns a random value {-1,0,+1}
    :return:
    """
    return math.floor((random.random() * 3) - 1)


def random_binary():
    """
    Returns a random value {0,+1}
    :return:
    """
    return math.floor((random.random() * 2))


f = open('vehicles.generated.csv', 'a')
for v_i in range(1, NUM_VEHICLES + 1):
    intersections = [
        (math.floor(random.random() * NUM_INTERSECTIONS_X), math.floor(random.random() * NUM_INTERSECTIONS_Y))]
    for i in range(0, NUM_INTERSECTIONS_PER_VEHICLE):
        intersections_last = intersections[-1]

        if intersections_last[0] == 0:
            x_change = random_binary()
        elif intersections_last[0] == NUM_INTERSECTIONS_X - 1:
            x_change = -random_binary()
        else:
            x_change = random_ternary()

        if x_change == 0:
            if intersections_last[1] == 0:
                y_change = 1
            elif intersections_last[1] == NUM_INTERSECTIONS_Y - 1:
                y_change = -1
            else:
                y_change = random_binary() * 2 - 1
        else:
            y_change = 0

        intersections_next = (intersections_last[0] + x_change, intersections_last[1] + y_change)

        intersections.append(intersections_next)

    s = str(v_i) + ";"
    rds = []
    for i in range(1, NUM_INTERSECTIONS_PER_VEHICLE):
        s_ = ""
        s_ += "i" + str(intersections[i - 1][0]) + str(intersections[i - 1][1])
        s_ += "i" + str(intersections[i][0]) + str(intersections[i][1])
        rds.append(s_)
    s += ",".join(rds)
    f.write(s + "\n")
f.close()
