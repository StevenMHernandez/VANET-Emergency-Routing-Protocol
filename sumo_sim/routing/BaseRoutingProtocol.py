class BaseRoutingProtocol:
    """Abstract base class for routing protocols."""

    def route_message(self, cur_fwdr, settings, vehicle_net, neighbors, cur_time, to_and_from_for_edge):
        """Gives message to all next forwarders.

        :param neighbors:
        :param cur_fwdr: current forwarder
        :param settings: protocol settings
        :param vehicle_net: vehicle network
        :param neighbors: list of neighbors for the given cur_fwdr
        :param cur_time: current simulation time
        :return:
        """

        # remains_forwarder = True

        if (self.should_continue_routing(settings, cur_fwdr, 0, to_and_from_for_edge)
                and self.should_remain_current_forwarder(cur_fwdr,
                                                         cur_time,
                                                         settings,
                                                         neighbors,
                                                         hop_num=0)):

            nxt_fwdrs = self.choose_next_forwarders(settings,
                                                    cur_fwdr,
                                                    neighbors,
                                                    to_and_from_for_edge,
                                                    hop_num=0)

            for nxt_fwdr in nxt_fwdrs:
                if not self.should_remain_current_forwarder_after_sharing():
                    vehicle_net[cur_fwdr.id].is_cur_fwdr = False
                    # remains_forwarder = False

                vehicle_net[nxt_fwdr.id].received_at = cur_time
                vehicle_net[nxt_fwdr.id].is_cur_fwdr = True
                cur_fwdr.msg.hop_cnt += 1
                vehicle_net[nxt_fwdr.id].msg = cur_fwdr.msg
                self.share_additional_data(cur_fwdr, nxt_fwdr)
        else:
            vehicle_net[cur_fwdr.id].is_cur_fwdr = False
            # remains_forwarder = False

        # return remains_forwarder

    @staticmethod
    def choose_next_forwarders(settings, f_curr, neighbors, to_and_from_for_edge, hop_num):
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
    def should_continue_routing(settings, cur_fwdr, hop_num, to_and_from_for_edge):
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


def _find_node_closest_to(intersection, neighbors, f_curr):
    """
    Find a node closest to a given intersection which
    1. has not received a warning-packet in the past
    2. is currently on the road segment
    3. Either:
        a. the current forwarder has been affected (thus not moving)
        b. appeared on the road segment before the current forwarder

    :param intersection:
    :param neighbors:
    :param f_curr:
    :return:
    """
    f_next = None
    f_next_passed_previous_intersection_at = f_curr.passed_previous_intersection_at

    for n in neighbors:
        has_not_received_packet = n.received_at is None
        is_on_road_segment = (n.cur_road == f_curr.cur_road)
        current_forwarder_has_been_affected = f_curr.affected_at is not None
        testing = f_next_passed_previous_intersection_at >= n.passed_previous_intersection_at

        if (has_not_received_packet
                and is_on_road_segment
                and (current_forwarder_has_been_affected or testing)):
            f_next = n
            f_next_passed_previous_intersection_at = n.passed_previous_intersection_at

    return f_next


def _calc_dist(isect0, isect1):
    """Calculates distance between two intersections.

    Distance is number of intersections required to get from
    one to the other.

    :param isect0: first intersection
    :param isect1: second intersection
    :return:
    """

    isect0_pos_x = int(isect0.name[1:2])
    isect0_pos_y = int(isect0.name[2:3])

    isect1_pos_x = int(isect1.name[1:2])
    isect1_pos_y = int(isect1.name[2:3])

    return abs(isect0_pos_x - isect1_pos_x) + abs(isect0_pos_y - isect1_pos_y)
