class BaseRoutingProtocol:
    """Abstract base class for routing protocols."""

    def route_message(self, f_curr, settings, vehicle_net, cur_time):
        """Gives message to all next forwarders.

        :param f_curr: current forwarder
        :param settings: protocol settings
        :param vehicle_net: vehicle network
        :param cur_time: current simulation time
        :return:
        """

        if (self.should_continue_routing(settings, f_curr.neighbors, 0)
                and self.should_remain_current_forwarder(f_curr,
                                                         cur_time,
                                                         settings,
                                                         f_curr.neighbors, 0)):

            next_forwarders = self.choose_next_forwarders(settings,
                                                          f_curr,
                                                          f_curr.neighbors,
                                                          hop_num=0)

            for f_next in next_forwarders:
                if not self.should_remain_current_forwarder_after_sharing():
                    vehicle_net[f_curr.id - 1].is_current_forwarder = False

                vehicle_net[f_next.id - 1].received_at = cur_time
                vehicle_net[f_next.id - 1].is_current_forwarder = True
                self.share_additional_data(f_curr, f_next)
        else:
            vehicle_net[f_curr.id - 1].is_current_forwarder = False

    @staticmethod
    def choose_next_forwarders(settings, f_curr, neighbors, hop_num):
        """Chooses the next forwarders.

        Next forwarders are based on the protocols settings, neighbors,
        and current hop number of message.

        :param f_curr: current forwarder
        :param settings: protocol settings
        :param neighbors: neighbors of current forwarder
        :param hop_num: current hop number of message
        :return: List of next forwarders
        """
        return NotImplemented

    @staticmethod
    def should_continue_routing(settings, neighbors, hop_num):
        return NotImplemented

    @staticmethod
    def should_remain_current_forwarder(f_curr, cur_time, settings, neighbors,
                                        hop_num):
        return NotImplemented

    @staticmethod
    def share_additional_data(src, dest):
        return NotImplemented

    @staticmethod
    def should_remain_current_forwarder_after_sharing():
        return NotImplemented


class UrbanRoutingProtocol(BaseRoutingProtocol):
    @staticmethod
    def choose_next_forwarders(settings, f_curr, neighbors, hop_num):
        """Chooses the next forwarder from the list of neighbors.

        This method returns a List despite having only one member
        because other routing protocols may have multiple forwarders.
        Returning a List helps with generalizing the interface when
        other protocols are involved.

        :param neighbors: List of neighbors
        :return: List containing next forwarder
        """

        ret_lst = []

        if f_curr.at_intersection:
            # Determine which road to send down next
            # Determine which vehicle is furthest on this road
            pass
        else:
            if f_curr.original_forwarder:
                # Determine destination (intersection) of packet
                f_curr.dest_intersection = f_curr.cur_road.start_node

            #
            # 1. Find node which is closest to the intersection
            #
            f_next = None
            f_next_passed_previous_intersection_at = f_curr.passed_previous_intersection_at
            for n in neighbors:
                if n.received_at is None:
                    if (n.cur_road.start_node == f_curr.dest_intersection and n.cur_road.end_node == f_curr.cur_road.end_node) and \
                            (f_curr.affected_at is not None or
                            f_next_passed_previous_intersection_at >= n.passed_previous_intersection_at):
                        f_next = n
                        f_next_passed_previous_intersection_at = n.passed_previous_intersection_at

            #
            # 2. Alternatively, find node which is headed towards the intersection (but on a different road)
            #
            if f_next is None:
                for n in neighbors:
                    if n.received_at is None:
                        if n.cur_road.end_node == f_curr.dest_intersection:
                            f_next = n

            if f_next is not None:
                ret_lst.append(f_next)

        return ret_lst

    @staticmethod
    def should_continue_routing(settings, neighbors, hop_num):
        return hop_num < settings["max_hops"]

    @staticmethod
    def should_remain_current_forwarder(f_curr, cur_time, settings, neighbors,
                                        hop_num):
        return True # or f_curr.received_at + settings["forwarder_ttl"] > cur_time

    @staticmethod
    def should_remain_current_forwarder_after_sharing():
        return False

    @staticmethod
    def share_additional_data(src, dest):
        if not dest.at_intersection:
            # Tell f_next (dest) which intersection to try sending towards
            dest.dest_intersection = src.dest_intersection
            src.dest_intersection = None



class Epidemic(BaseRoutingProtocol):
    @staticmethod
    def choose_next_forwarders(settings, f_curr, neighbors, hop_num):
        ret_lst = []

        for n in neighbors:
            if n.received_at is None and not n.original_forwarder:
                ret_lst.append(n)

        return ret_lst

    @staticmethod
    def should_continue_routing(settings, neighbors, hop_num):
        return True

    @staticmethod
    def should_remain_current_forwarder(f_curr, cur_time, settings, neighbors,
                                        hop_num):
        return True

    @staticmethod
    def should_remain_current_forwarder_after_sharing():
        return True

    @staticmethod
    def share_additional_data(src, dest):
        pass
