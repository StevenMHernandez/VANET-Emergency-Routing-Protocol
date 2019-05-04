from sumo_sim.routing.BaseRoutingProtocol import _calc_dist
from sumo_sim.routing.UrbanRoutingProtocol import UrbanRoutingProtocol


class UrbanRoutingIntersection(UrbanRoutingProtocol):
    """Urban Routing Protocol that terminates based on intersection count."""

    @staticmethod
    def should_continue_routing(settings, cur_fwdr, hop_num, to_and_from_for_edge):
        """Continues routing until max hop count is reached.

        :param to_and_from_for_edge:
        :param settings: settings for routing protocol
        :param cur_fwdr: current forwarder
        :param hop_num: current hop count of message
        :return: if the current forwarder should continue routing
        """

        dist = _calc_dist(to_and_from_for_edge[cur_fwdr.msg.src_rd][0],
                          cur_fwdr.msg.dst_isect)

        return dist < settings["max_ints"]
