from sumo_sim.routing.BaseRoutingProtocol import BaseRoutingProtocol, _find_node_closest_to


class UrbanRoutingProtocol(BaseRoutingProtocol):
    """ABC for Urban Routing Protocol."""

    @staticmethod
    def choose_next_forwarders(settings, f_curr, neighbors, to_and_from_for_edge, hop_num):
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

            # Find interested neighbors
            intrstd_neighbors = [n for n in neighbors
                                 if n.route_contains_rd(settings, f_curr.msg.src_rd)]

            # 1. Determine which road(s) to send down next
            feed_ratios = {}

            for n in intrstd_neighbors:
                if n.cur_road not in feed_ratios:
                    feed_ratios[n.cur_road] = 0
                feed_ratios[n.cur_road] += 1

            for r in feed_ratios:
                if feed_ratios[r] / len(neighbors) > settings["min_feed_ratio"]:
                    # 2. Determine which vehicle is furthest on this road
                    # (closest to next intersection)
                    f_next = _find_node_closest_to(intersection=to_and_from_for_edge[r][0],
                                                   neighbors=intrstd_neighbors,
                                                   f_curr=f_curr)

                    if f_next is not None:
                        ret_lst.append(f_next)
        else:
            # Moved this to the vehicle's routing update method
            # if f_curr.original_forwarder:
            #     # Determine destination (intersection) of packet
            #     f_curr.dest_intersection = f_curr.cur_road.start_node

            dst_isect = f_curr.msg.dst_isect

            # Find interested neighbors
            intrstd_neighbors = [n for n in neighbors
                                 if n.route_contains_rd(settings, f_curr.msg.src_rd)]

            # 1. Find node which is closest to the intersection
            f_next = _find_node_closest_to(intersection=dst_isect,
                                           neighbors=intrstd_neighbors,
                                           f_curr=f_curr)

            # Wouldn't this be another variant to our protocol?
            # 2. Alternatively, find node which is headed towards the
            # intersection (but on a different road)
            # if f_next is None:
            #     for n in neighbors:
            #         if n.received_at is None:
            #             if n.cur_road.end_node == dst_isect:
            #                 f_next = n

            if f_next is not None:
                ret_lst.append(f_next)

        return ret_lst

    @staticmethod
    def should_continue_routing(settings, cur_fwdr, hop_num, to_and_from_for_edge):
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
            dest.msg.dst_isect = src.msg.dst_isect
            src.msg.dst_isect = None
