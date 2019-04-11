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
            if v.affected_at is not None and v.received_at is not None:
                n += 1

        return n

    @staticmethod
    def get_average_time_to_react(vehicle_net):
        n = 0
        s = 0

        for v in vehicle_net:
            if v.affected_at is not None and \
                    v.received_at is not None and \
                    v.affected_at >= v.received_at:
                n += 1
                s += v.affected_at - v.received_at

        return 0 if n == 0 else s / n

    @staticmethod
    def run(t, vehicle_net):
        s = "\n".join(["========",
                       "Time: {}",
                       "# affected: {}",
                       "# receiving message: {}",
                       "# affected and received: {}",
                       "AVG time to react: {}",
                       "",
                       ])

        return s.format(t,
                        Evaluations.get_num_affected(vehicle_net),
                        Evaluations.get_num_received(vehicle_net),
                        Evaluations.get_num_affected_and_received(vehicle_net),
                        Evaluations.get_average_time_to_react(vehicle_net),
                        )
