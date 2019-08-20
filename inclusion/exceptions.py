# credit: https://www.programiz.com/python-programming/user-defined-exception

class Error(Exception):
   """Base class for other exceptions"""
   pass

class UndefinedTrait(Error):
   """Raised when querying for a trait that has not been defined"""
   pass

class NonBooleanQueryValue(Error):
   """Raised when querying for a trait using a non-boolean value"""
   pass

class TraitNotUnique(Error):
   """Raised when defining a trait with a name that already exists for the TraitSet"""
   pass

class ArgumentNotCallable(Error):
   """Raised when function defined for trait is not callable"""
   pass
