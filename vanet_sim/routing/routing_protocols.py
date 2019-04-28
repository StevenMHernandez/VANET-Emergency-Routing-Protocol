class Message:
    """POD class representing the incident message."""

    def __init__(self, src_isect, dst_isect):
        """Custom constructor for Message object.

        :param src_isect: start intersection of incident road
        :param dst_isect: start intersection of current road
        """
        self.src_isect = src_isect
        self.dst_isect = dst_isect
        self.hop_cnt = 0


class BaseRoutingProtocol:
    """Abstract base class for routing protocols."""

    def route_message(self, cur_fwdr, settings, vehicle_net, cur_time):
        """Gives message to all next forwarders.

        :param cur_fwdr: current forwarder
        :param settings: protocol settings
        :param vehicle_net: vehicle network
        :param cur_time: current simulation time
        :return:
        """

        if (self.should_continue_routing(settings, cur_fwdr.neighbors, 0)
                and self.should_remain_current_forwarder(cur_fwdr,
                                                         cur_time,
                                                         settings,
                                                         cur_fwdr.neighbors,
                                                         hop_num=0)):

            nxt_fwdrs = self.choose_next_forwarders(settings,
                                                    cur_fwdr,
                                                    cur_fwdr.neighbors,
                                                    hop_num=0)

            for nxt_fwdr in nxt_fwdrs:
                if not self.should_remain_current_forwarder_after_sharing():
                    vehicle_net[cur_fwdr.id - 1].is_cur_fwdr = False

                vehicle_net[nxt_fwdr.id - 1].received_at = cur_time
                vehicle_net[nxt_fwdr.id - 1].is_cur_fwdr = True
                self.share_additional_data(cur_fwdr, nxt_fwdr)
        else:
            vehicle_net[cur_fwdr.id - 1].is_cur_fwdr = False

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
    """ABC for Urban Routing Protocol."""

    @staticmethod
    def find_node_closest_to(intersection, neighbors, f_curr):
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
            is_on_road_segment = (n.cur_road.start_node == intersection
                                  and n.cur_road.end_node == f_curr.cur_road.end_node)
            current_forwarder_has_been_affected = f_curr.affected_at is not None
            testing = f_next_passed_previous_intersection_at >= n.passed_previous_intersection_at

            if (has_not_received_packet
                    and is_on_road_segment
                    and (current_forwarder_has_been_affected or testing)):

                f_next = n
                f_next_passed_previous_intersection_at = n.passed_previous_intersection_at

        return f_next

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

            # 1. Determine which road to send down next
            FR = {}
            R_nxt = None
            for n in neighbors:
                if n.cur_road not in FR:
                    FR[n.cur_road] = 0
                FR[n.cur_road] += 1

                # Determine R_nxt
                if R_nxt is not None and FR[n.cur_road] > FR[R_nxt]:
                    R_nxt = n.cur_road

            # 2. Determine which vehicle is furthest on this road
            # (closest to next intersection)
            f_next = None
            if R_nxt is not None:
                f_next = UrbanRoutingProtocol.find_node_closest_to(intersection=R_nxt.end_node,
                                                                   neighbors=neighbors,
                                                                   f_curr=f_curr)

            if f_next is not None:
                ret_lst.append(f_next)
        else:
            if f_curr.original_forwarder:
                # Determine destination (intersection) of packet
                f_curr.dest_intersection = f_curr.cur_road.start_node

            # 1. Find node which is closest to the intersection
            f_next = UrbanRoutingProtocol.find_node_closest_to(intersection=f_curr.dest_intersection,
                                                               neighbors=neighbors,
                                                               f_curr=f_curr)

            # 2. Alternatively, find node which is headed towards the
            # intersection (but on a different road)
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
        return NotImplemented

    @staticmethod
    def should_remain_current_forwarder(f_curr, cur_time, settings, neighbors,
                                        hop_num):
        return True

    @staticmethod
    def should_remain_current_forwarder_after_sharing():
        return False

    @staticmethod
    def share_additional_data(src, dest):
        if not dest.at_intersection:
            # Tell f_next (dest) which intersection to try sending towards
            dest.dest_intersection = src.dest_intersection
            src.dest_intersection = None


class UrbanRoutingHops(UrbanRoutingProtocol):
    """Urban Routing Protocol that terminates based on hop count."""

    @staticmethod
    def should_continue_routing(settings, neighbors, hop_num):
        return hop_num < settings["max_hops"]


class UrbanRoutingIntersection(UrbanRoutingProtocol):
    """Urban Routing Protocol that terminates based on intersection count."""

    @staticmethod
    def should_continue_routing(settings, neighbors, hop_num):
        return hop_num < settings["max_ints"]


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


def _calc_dist(isect0, isect1):
    """Calculates distance between two intersections.

    :param isect0: first intersection
    :param isect1: second intersection
    :return:
    """

    isect0_pos_x = int(isect0.name[1:2])
    isect0_pos_y = int(isect0.name[2:3])

    isect1_pos_x = int(isect1.name[1:2])
    isect1_pos_y = int(isect1.name[2:3])

    return abs(isect0_pos_x - isect1_pos_x) + (isect0_pos_y - isect1_pos_y)
