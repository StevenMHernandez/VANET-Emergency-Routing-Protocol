"""Contains code to run the simulations."""

__author__ = 'Adam Morrissett'


class Simulation:
    """Performs a simulation."""

    def __init__(self, d_time, road_net, vehicle_net):
        """Custom constructor that initializes parameters.

        :param d_time: simulation time resolution
        :param road_net: filepath of the road network config file
        :param vehicle_net: filepath of the vehicle network config file
        """
        self.cur_time = 0
        self.d_time = d_time
        self.road_net = road_net
        self.vehicle_net = vehicle_net

    def run(self, time_duration):
        """Executes the simulation for the specified duration.

        This is on top of previous simulation time.
        """

        print(f'Starting simulation from t = {self.cur_time:.3f}')

        while self.cur_time < time_duration:
            self.vehicle_net
            self.cur_time += self.d_time
