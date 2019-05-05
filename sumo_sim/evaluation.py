__author__ = 'Steven M. Hernandez'


class Evaluations:
    @staticmethod
    def get_num_affected(vehicle_net):
        n = 0

        for v in vehicle_net:
            if v.affected_at is not None:
                n += 1

        return n

    @staticmethod
    def get_num_received(vehicle_net):
        n = 0

        for v in vehicle_net:
            if v.received_at is not None:
                n += 1

        return n

    @staticmethod
    def get_num_affected_and_received(vehicle_net):
        n = 0

        for v in vehicle_net:
            if (v.last_road_moving_on is not None
                    and v.received_before_incident_road):
                n += 1

        return n

    @staticmethod
    def get_average_time_to_react(vehicle_net):
        n = 0
        s = 0

        for v in vehicle_net:
            if (v.affected_at
                    and v.last_road_moving_on is not None
                    and v.received_before_incident_road):
                n += 1
                s += v.affected_at - v.received_at

        return 0 if n == 0 else s / n

    @staticmethod
    def run(t, vehicle_net):
        s = "\n".join(["========",
                       "Time: {}",
                       "# affected: {}",
                       "# receiving message: {}",
                       "# affected and received early: {}",
                       "AVG time to react: {}",
                       "",
                       ])

        return s.format(t,
                        Evaluations.get_num_affected(vehicle_net),
                        Evaluations.get_num_received(vehicle_net),
                        Evaluations.get_num_affected_and_received(vehicle_net),
                        Evaluations.get_average_time_to_react(vehicle_net),
                        )

    @staticmethod
    def write_to(directory, t, vehicle_net):
        if t == 0:
            f = open(directory + "evaluation.csv", "w")
            f.write("time,num_affected,num_received,num_affected_and_received,avg_time_to_react\n")
            f.close()
        f = open(directory + "evaluation.csv", "a")
        f.write(",".join(str(x) for x in [
            t,
            Evaluations.get_num_affected(vehicle_net),
            Evaluations.get_num_received(vehicle_net),
            Evaluations.get_num_affected_and_received(vehicle_net),
            Evaluations.get_average_time_to_react(vehicle_net),
        ]) + "\n")
