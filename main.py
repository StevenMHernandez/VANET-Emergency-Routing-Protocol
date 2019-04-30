"""Top-level script to run the simulation.

"""


__author__ = 'Adam Morrissett', 'Steven M. Hernandez'


from vanet_sim import simulation, vehicle_net, road_net


road_map = road_net.RoadMap(intersection_file='intersections.generated.csv',
                            road_file='roads.generated.csv')

vehicles = vehicle_net.build_vehicle_net(filepath='vehicles.200.generated.csv',
                                         road_map=road_map)

sim = simulation.Simulation(d_time=0.5,
                            road_map=road_map,
                            vehicle_net=vehicles)

sim.run(time_duration=100)
