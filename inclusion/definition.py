class Definition():
    """Definitions are how traits are defined.
    Definitions hold the bitflag associated with the trait,
    as well as the function which defines the trait."""

    def __init__(self, integer, func):
        # the bitflag should be a power of 2 because that ensures uniqueness
        # when combining multiple definitions into a bitmask.
        # `<< N` operator is bitwise shift left which, for integers, is the same as
        # "multiply by 2 to the N power"
        self.flag = 1 << integer

        # func is persisted for later access
        self.func = func
