class UrbanRoutingProtocol:
    @staticmethod
    def choose_next_forwarder(neighbors):
        for n in neighbors:
            if n.received_at is None and n.affected_at is None:
                return n
        return None
