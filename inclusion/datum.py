class Datum():
    """Container for an analyzed datum with an assigned bitmask"""

    def __init__(self, value, bitmask):
        # persist value for later access
        self.value = value

        # bitmask is the sum of bitflags for the traits that are
        # present for the `value`
        self.bitmask = bitmask
