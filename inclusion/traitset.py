from functools import reduce
from .exceptions import UndefinedTrait, TraitNotUnique, NonBooleanQueryValue, ArgumentNotCallable
from .definition import Definition
from .datum import Datum

# TraitSet is the primary public class in the Inclusion API.
# It allows clients to define traits on a dataset,
# analyze a dataset for the inclusion/exclusion of the defined traits,
# and query the dataset for a subset of traits.
class TraitSet():
    def __init__(self):
        # `dataset` stores the analyzed dataset passed to `analyze()`
        # type: Datum[]
        self.dataset = []

        # traits are defined with `define_trait()` method.
        # A key/value pair matches a trait name (key) to the Definition (value)
        self.trait_definitions = {}

    # `define_trait` links a uniquely named trait (`name` argument)
    # to a lambda or function that will operate on data to assert
    # the presence or absence of the trait.
    #
    # Lambdas/functions passed to `define_trait` should always return a boolean.
    # If they do not return a boolean, user should be cognizant of how returned
    # values coerce to boolean.
    def define_trait(self, name, func):
        """Define a unique trait with a function that will operate on data"""

        if name in self.trait_definitions:
           raise TraitNotUnique("Trait name must be unique. `{}` already defined in this TraitSet".format(name))

        if not hasattr(func, '__call__'):
            raise ArgumentNotCallable("Trait function must be callable (i.e. a lambda or a function). `{}` does not implement `__call__` method".format(func))

        self.trait_definitions[name] = Definition(len(self.trait_definitions), func)

    # TODO: not ideal to iterate over any object that implements __iter__;
    #       should API specify that `data` is always assumed to be iterable? (and raise error if not?)
    def analyze(self, data, purge = False):
        """Analyze data against defined traits"""

        if purge:
            self.__purge_dataset()

        # if iterable, process all items in collection
        if hasattr(data, '__iter__'):
            self.dataset.extend(
                # are these equivalent??
                # [self.__analyze_datum(datum) for datum in data]
                map(self.__analyze_datum, data)
            )
        else:
            self.dataset.extend([self.__analyze_datum(data)])

    # Analyze datum for each defined trait.
    # return: Datum
    def __analyze_datum(self, datum):
        # sum bitmask for traits that are present on datum
        bitmask = 0
        for value in self.trait_definitions.values():
            if value.func(datum):
                bitmask |= value.flag

        # returned Trait collects analyzed datum and
        # bitmask representing present traits
        return Datum(datum, bitmask)

    def __purge_dataset(self):
        self.dataset = []

    def pickle(self, filepath = None):
        print("Method not yet implemented. Goal is to be able to save a TraitSet with all analyzed data and defined traits")

    def dump(self, filepath = None):
        print("Method not yet implemented. Goal is to be able to save the analyzed data in some serializable form")

    # returns list of values that match the requested traits
    def query(self, traits = {}):
        """Query the dataset for data that includes the requested `traits`"""

        # Traits must be defined with `define_trait` before they can be queried
        if any(map(lambda key: key not in self.trait_definitions, traits.keys())):
            undefined_traits = [trait for trait in traits.keys() if trait not in self.trait_definitions]
            raise UndefinedTrait("Cannot query for traits that have not been defined. Traits `{}` are not defined".format(', '.join(undefined_traits)))

        # Requested traits must be boolean: True for present, False for absent
        if any(map(lambda value: not isinstance(value, bool), traits.values())):
            non_bool_values = [trait for trait, value in traits.items() if not isinstance(value, bool)]
            raise NonBooleanQueryValue("Trait values must be boolean. Traits `{}` do not have boolean values".format(', '.join(non_bool_values)))

        # return list of values if they are included in the requested traits
        positive_flag, negative_flag = self.__collect_bitmasks(traits)
        return [datum.value for datum in self.dataset if self.__is_included(datum.bitmask, positive_flag, negative_flag)]

    def __collect_bitmasks(self, traits = {}):
        # calculate positive bitflag
        # This represents the sum of the traits that are requested to be True
        positive_traits = [k for k, v in traits.items() if v]
        positive_flag = self.__sum_bitmask(positive_traits)

        # calculate negative bitmask
        # This represents the sum of the traits that are requested to be False
        negative_traits = [k for k, v in traits.items() if not v]
        negative_flag = self.__sum_bitmask(negative_traits)

        return [positive_flag, negative_flag]

    def __sum_bitmask(self, traits):
        return reduce(lambda all, trait: all + self.trait_definitions[trait].flag, traits, 0)

    def __is_included(self, mask, positive, negative = 0):
        """Check if a mask includes a positive number and excludes a negative number"""
        return mask & positive == positive and mask & negative == 0
