from sumo_sim.routing.UrbanRoutingProtocol import UrbanRoutingProtocol


class UrbanRoutingHops(UrbanRoutingProtocol):
    """Urban Routing Protocol that terminates based on hop count."""

    @staticmethod
    def should_continue_routing(settings, cur_fwdr, hop_num, to_and_from_for_edge):
        """Continues routing until max hop count is reached.

        :param to_and_from_for_edge:
        :param settings: settings for routing protocol
        :param cur_fwdr: current forwarder
        :param hop_num: current hop count of message
        :return: if the current forwarder should continue routing
        """

        return cur_fwdr.msg.hop_cnt < settings["max_hops"]
