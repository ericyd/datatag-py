# credit: https://www.programiz.com/python-programming/user-defined-exception

class Error(Exception):
   """Base class for other exceptions"""
   pass

class UndefinedTag(Error):
   """Raised when querying for a tag that has not been defined"""
   pass

class NonBooleanQueryValue(Error):
   """Raised when querying for a tag using a non-boolean value"""
   pass

class TagNotUnique(Error):
   """Raised when defining a tag with a name that already exists for the TagSet"""
   pass

class ArgumentNotCallable(Error):
   """Raised when function defined for tag is not callable"""
   pass

class DataNotIterable(Error):
   """Raised when data passed to analyze is not iterable"""
   pass