from sumo_sim.routing.BaseRoutingProtocol import BaseRoutingProtocol, _find_node_closest_to


class InterestedOnlyProtocol(BaseRoutingProtocol):
    """ABC for Interested Party Only Protocol."""

    @staticmethod
    def choose_next_forwarders(settings, f_curr, neighbors, to_and_from_for_edge, hop_num):
        """Chooses the next forwarder from the list of neighbors.

        :param neighbors: List of neighbors
        :return: List containing next forwarder
        """

        intrstd_neighbors = [n for n in neighbors
                             if (n.route_contains_rd(settings, f_curr.msg.src_rd)
                                 and n.received_at is None
                                 and n.affected_at is None)]
        return intrstd_neighbors

    @staticmethod
    def should_remain_current_forwarder(f_curr, cur_time, settings, neighbors,
                                        hop_num):
        return True

    @staticmethod
    def should_remain_current_forwarder_after_sharing():
        return False
