"""Create random roads and vehicles which would not be possible by hand.

"""
import math
import random

__author__ = 'Adam Morrissett', 'Steven M. Hernandez'

NUM_INTERSECTIONS_X = 8
NUM_INTERSECTIONS_Y = 8
NUM_VEHICLES = 200
NUM_INTERSECTIONS_PER_VEHICLE = 20
OBSTRUCTION_START = (5, 2)
OBSTRUCTION_END = (6, 2)
RANDOM_MOVEMENT = False # if False, roads act as one-way roads

open('intersections.generated.csv', 'w').close()
open('roads.generated.csv', 'w').close()
open('vehicles.200.generated.csv', 'w').close()

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


f = open('vehicles.200.generated.csv', 'a')
for v_i in range(1, NUM_VEHICLES + 1):
    intersections = [
        (math.floor(random.random() * NUM_INTERSECTIONS_X), math.floor(random.random() * NUM_INTERSECTIONS_Y))]
    for i in range(0, NUM_INTERSECTIONS_PER_VEHICLE):
        intersections_last = intersections[-1]

        if RANDOM_MOVEMENT:
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
        else:
            # Urban Roadways (one-way streets)

            #    x: 0 1 2 3 4 5 6 7 8 9
            # y: 0 ->->->->->->->->->->
            #    1 <-<-<-<-<-<-<-<-<-<-
            #    2 ->->->->->->->->->->
            #    3 <-<-<-<-<-<-<-<-<-<-
            #    4 ->->->->->->->->->->
            #    5 <-<-<-<-<-<-<-<-<-<-
            #    6 ->->->->->->->->->->
            #    7 <-<-<-<-<-<-<-<-<-<-
            #    8 ->->->->->->->->->->
            #    9 <-<-<-<-<-<-<-<-<-<-

            #    x: 0 1 2 3 4 5 6 7 8 9
            # y: 0  ^ | ^ | ^ | ^ | ^ |
            #    1  | ↓ | ↓ | ↓ | ↓ | ↓
            #    2  ^ | ^ | ^ | ^ | ^ |
            #    3  | ↓ | ↓ | ↓ | ↓ | ↓
            #    4  ^ | ^ | ^ | ^ | ^ |
            #    5  | ↓ | ↓ | ↓ | ↓ | ↓
            #    6  ^ | ^ | ^ | ^ | ^ |
            #    7  | ↓ | ↓ | ↓ | ↓ | ↓
            #    8  ^ | ^ | ^ | ^ | ^ |
            #    9  | ↓ | ↓ | ↓ | ↓ | ↓

            def is_even(n):
                return n % 2 == 0


            if not is_even(NUM_INTERSECTIONS_X) or not is_even(NUM_INTERSECTIONS_Y):
                raise Exception("# of Intersections cannot be odd or vehicles will become stuck.")

            x = intersections_last[0]
            y = intersections_last[1]

            only_x_movement = (y == 0 and is_even(x)) or (y >= NUM_INTERSECTIONS_Y - 1 and not is_even(x))
            only_y_movement = (x == 0 and not is_even(y)) or (x >= NUM_INTERSECTIONS_X - 1 and is_even(y))

            movement = random_binary()
            if (movement == 0 or only_x_movement) and not only_y_movement:
                x_change = 1 if is_even(y) else -1
                y_change = 0
            else:
                x_change = 0
                y_change = -1 if is_even(x) else 1

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
