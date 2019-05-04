class Message:
    """POD class representing the incident message."""

    def __init__(self, src_rd, dst_isect):
        """Custom constructor for Message object.

        :param src_rd: the incident road
        :param dst_isect: start intersection of current road
        """

        self.src_rd = src_rd
        self.dst_isect = dst_isect
        self.hop_cnt = 0