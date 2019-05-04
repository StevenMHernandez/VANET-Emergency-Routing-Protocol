from sumo_sim.routing.BaseRoutingProtocol import BaseRoutingProtocol, _find_node_closest_to


class GyTar(BaseRoutingProtocol):
    @staticmethod
    def choose_next_forwarders(settings, f_curr, neighbors, to_and_from_for_edge, hop_num):
        ret_lst = []

        if f_curr.at_intersection:

            # 1. Determine which road to send down next
            feed_ratios = {}
            nxt_rd = None

            for n in neighbors:
                if n.cur_road is f_curr.cur_road:
                    continue

                if n.cur_road not in feed_ratios:
                    feed_ratios[n.cur_road] = 0
                feed_ratios[n.cur_road] += 1

                # Determine nxt_rd
                if (nxt_rd is None
                        or feed_ratios[n.cur_road] > feed_ratios[nxt_rd]):
                    nxt_rd = n.cur_road

            # 2. Determine which vehicle is furthest on this road
            # (closest to next intersection)
            f_next = None
            if nxt_rd is not None:
                f_next = _find_node_closest_to(intersection=nxt_rd.end_node,
                                               neighbors=neighbors,
                                               f_curr=f_curr)

            if f_next is not None:
                ret_lst.append(f_next)
        else:
            dst_isect = f_curr.msg.dst_isect
            f_next = _find_node_closest_to(intersection=dst_isect,
                                           neighbors=neighbors,
                                           f_curr=f_curr)

            if f_next is not None:
                ret_lst.append(f_next)

        return ret_lst

    @staticmethod
    def should_continue_routing(settings, neighbors, hop_num, to_and_from_for_edge):
        return True

    @staticmethod
    def should_remain_current_forwarder(f_curr, cur_time, settings, neighbors,
                                        hop_num):
        return True

    @staticmethod
    def should_remain_current_forwarder_after_sharing():
        return False

    @staticmethod
    def share_additional_data(src, dest):
        pass

