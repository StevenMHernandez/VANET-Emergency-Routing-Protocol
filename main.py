"""Top-level script to run the simulation.

"""

__author__ = 'Adam Morrissett', 'Steven M. Hernandez'

from vanet_sim import simulation, vehicle_net, road_net

# sim = simulation.Simulation(d_time=1)
# sim.run(time_duration=100)
# sim.run(time_duration=100)

road_map = road_net.build_road_map(filepath='road_net.csv')
print(road_map)

vehicles = vehicle_net.build_vehicle_net(filepath='vehicle_net.csv',
                                         road_map=road_map)
print(vehicles)

# r1 = road_net.Road(start_node='i1',
#                    end_node='i2',
#                    length=5,
#                    spd_lim=1,
#                    is_obstructed=False)
#
# r2 = road_net.Road(start_node='i2',
#                    end_node='i3',
#                    length=5,
#                    spd_lim=1,
#                    is_obstructed=False)
#
# r3 = road_net.Road(start_node='i3',
#                    end_node='i4',
#                    length=5,
#                    spd_lim=1,
#                    is_obstructed=False)
#
# car = vehicle_net.Vehicle(node_id=1, route=[r1, r2, r3])
# for i in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]:
#     car.update(i)
