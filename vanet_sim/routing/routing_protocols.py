class BaseRoutingProtocol:
    def route_message(self, f_curr, settings, vehicle_net, cur_time):
        if self.should_continue_routing(settings, f_curr.neighbors, 0) and self.should_remain_current_forwarder(f_curr, cur_time, settings, f_curr.neighbors, 0):
            next_forwarders = self.choose_next_forwarders(settings, f_curr.neighbors, 0)

            for f_next in next_forwarders:
                if not self.should_remain_current_forwarder(f_curr, cur_time, settings, f_curr.neighbors, 0):
                    vehicle_net[f_curr.id - 1].is_current_forwarder = False
                vehicle_net[f_next.id - 1].received_at = cur_time
                vehicle_net[f_next.id - 1].is_current_forwarder = True
        else:
            vehicle_net[f_curr.id - 1].is_current_forwarder = False

    @staticmethod
    def choose_next_forwarders(settings, neighbors, hop_num):
        return []

    @staticmethod
    def should_continue_routing(settings, neighbors, hop_num):
        return True

    @staticmethod
    def should_remain_current_forwarder(f_curr, cur_time, settings, neighbors, hop_num):
        return False


class UrbanRoutingProtocol(BaseRoutingProtocol):
    @staticmethod
    def choose_next_forwarders(settings, neighbors, hop_num):
        """Chooses the next forwarder from the list of neighbors.

        This method returns a List despite having only one member
        because other routing protocols may have multiple forwarders.
        Returning a List helps with generalizing the interface when
        other protocols are involved.

        :param neighbors: List of neighbors
        :return: List containing next forwarder
        """

        ret_lst = []

        # if settings["max_hops"] <= hop_num:
        for n in neighbors:
            if n.received_at is None and n.affected_at is None:
                ret_lst.append(n)
                break

        return ret_lst

    @staticmethod
    def should_continue_routing(settings, neighbors, hop_num):
        return hop_num < settings["max_hops"]

    @staticmethod
    def should_remain_current_forwarder(f_curr, cur_time, settings, neighbors, hop_num):
        return f_curr.received_at + settings["forwarder_ttl"] > cur_time


class Epidemic(BaseRoutingProtocol):
    @staticmethod
    def choose_next_forwarders(settings, neighbors, hop_num):
        ret_lst = []

        for n in neighbors:
            if n.received_at is None and not n.original_forwarder:
                ret_lst.append(n)

        return ret_lst

    @staticmethod
    def should_remain_current_forwarder(f_curr, cur_time, settings, neighbors, hop_num):
        return True
