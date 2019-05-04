from sumo_sim.routing.BaseRoutingProtocol import BaseRoutingProtocol


class Epidemic(BaseRoutingProtocol):
    @staticmethod
    def choose_next_forwarders(settings, f_curr, neighbors, to_and_from_for_edge, hop_num):
        ret_lst = []

        for n in neighbors:
            if n.received_at is None and not n.original_forwarder:
                ret_lst.append(n)

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
        return True

    @staticmethod
    def share_additional_data(src, dest):
        pass

