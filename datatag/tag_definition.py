class TagDefinition():
    """TagDefinitions are how tags are defined.
    TagDefinitions hold the bitflag associated with the tag,
    as well as the function which defines the tag."""

    def __init__(self, integer, func):
        # the bitflag should be a power of 2 because that ensures uniqueness
        # when combining multiple definitions into a bitmask.
        # `<< N` operator is bitwise shift left which, for integers, is the same as
        # "multiply by 2 to the N power"
        self.flag = 1 << integer

        # func is persisted for later access
        self.func = func
