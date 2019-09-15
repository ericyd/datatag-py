from functools import reduce
from .exceptions import UndefinedTag, TagNotUnique, NonBooleanQueryValue, ArgumentNotCallable, DataNotIterable
from .tag_definition import TagDefinition
from .tagged_datum import TaggedDatum

# TagSet is the primary public class in the Inclusion API.
class TagSet():
    """Define tags on a dataset,
    analyze a dataset for the inclusion/exclusion of the defined tags,
    and query the dataset for a subset of tags."""

    def __init__(self):
        # `dataset` stores the analyzed dataset passed to `analyze()`
        # type: TaggedDatum[]
        self.dataset = []

        # tags are defined with `define_tag()` method.
        # A key/value pair matches a tag name (key) to the TagDefinition (value)
        self.tag_definitions = {}

    # `define_tag` links a uniquely named tag (`name` argument)
    # to a lambda or function that will operate on data to assert
    # the presence or absence of the tag.
    #
    # Lambdas/functions passed to `define_tag` should always return a boolean.
    # If they do not return a boolean, user should be cognizant of how returned
    # values coerce to boolean.
    def define_tag(self, name, func):
        """Define a unique tag with a function that will operate on data"""

        if name in self.tag_definitions:
           raise TagNotUnique("Tag name must be unique. `{}` already defined in this TagSet".format(name))

        if not hasattr(func, '__call__'):
            raise ArgumentNotCallable("Tag function must be callable (i.e. a lambda or a function). `{}` does not implement `__call__` method".format(func))

        self.tag_definitions[name] = TagDefinition(len(self.tag_definitions), func)

    def analyze(self, data = [], purge = False):
        """Analyze data against defined tags"""

        if not hasattr(data, '__iter__'):
            raise DataNotIterable("Data must be iterable. Argument data: `{}` does not implement `__iter__`".format(data))

        if purge:
            self.__purge_dataset()

        # re-process existing data and append with new data
        self.dataset = [self.__analyze_datum(d.value) for d in self.dataset]
        self.dataset.extend(map(self.__analyze_datum, data))

    # Analyze datum for each defined tag.
    # return: TaggedDatum
    def __analyze_datum(self, datum):
        # sum bitmask for tags that are present on datum
        bitmask = 0
        for value in self.tag_definitions.values():
            if value.func(datum):
                bitmask |= value.flag

        # returned Tag collects analyzed datum and
        # bitmask representing present tags
        return TaggedDatum(datum, bitmask)

    def __purge_dataset(self):
        self.dataset = []

    # returns list of values that match the requested tags
    def query(self, tags = {}):
        """Query the dataset for data that includes the requested `tags`"""

        # Tags must be defined with `define_tag` before they can be queried
        if any(map(lambda key: key not in self.tag_definitions, tags.keys())):
            undefined_tags = [tag for tag in tags.keys() if tag not in self.tag_definitions]
            raise UndefinedTag("Cannot query for tags that have not been defined. Tags `{}` are not defined".format(', '.join(undefined_tags)))

        # Requested tags must be boolean: True for present, False for absent
        if any(map(lambda value: not isinstance(value, bool), tags.values())):
            non_bool_values = [tag for tag, value in tags.items() if not isinstance(value, bool)]
            raise NonBooleanQueryValue("Tag values must be boolean. Tags `{}` do not have boolean values".format(', '.join(non_bool_values)))

        # return list of values if they are included in the requested tags
        positive_flag, negative_flag = self.__collect_bitmasks(tags)
        return [datum.value for datum in self.dataset if self.__is_included(datum.bitmask, positive_flag, negative_flag)]

    def __collect_bitmasks(self, tags = {}):
        # calculate positive bitflag
        # This represents the sum of the tags that are requested to be True
        positive_tags = [k for k, v in tags.items() if v]
        positive_flag = self.__sum_bitmask(positive_tags)

        # calculate negative bitmask
        # This represents the sum of the tags that are requested to be False
        negative_tags = [k for k, v in tags.items() if not v]
        negative_flag = self.__sum_bitmask(negative_tags)

        return [positive_flag, negative_flag]

    def __sum_bitmask(self, tags):
        return reduce(lambda all, tag: all + self.tag_definitions[tag].flag, tags, 0)

    def __is_included(self, mask, positive, negative = 0):
        """Check if a mask includes a positive number and excludes a negative number"""
        return mask & positive == positive and mask & negative == 0
