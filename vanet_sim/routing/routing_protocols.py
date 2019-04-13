class UrbanRoutingProtocol:
    @staticmethod
    def choose_next_forwarders(neighbors):
        """Chooses the next forwarder from the list of neighbors.

        This method returns a List despite having only one member
        because other routing protocols may have multiple forwarders.
        Returning a List helps with generalizing the interface when
        other protocols are involved.

        :param neighbors: List of neighbors
        :return: List containing next forwarder
        """

        ret_lst = []

        for n in neighbors:
            if n.received_at is None and n.affected_at is None:
                ret_lst.append(n)
                break

        return ret_lst


class Epidemic:
    @staticmethod
    def choose_next_forwarders(neighbors):
        ret_lst = []

        for n in neighbors:
            if n.received_at is None and not n.original_forwarder:
                ret_lst.append(n)

        return ret_lst
