# DataTag
Lightweight, flexible data tagging and querying

## Examples

Run `make example` or `python3 example.py` for annotated example script utilizing the package.

## Tests

The core logic is well tested in `tests/test_tagset.py`

Run with:

```
make test
```

or

```
python3 -m unittest
```

## API

### TagSet

The only class exported directly at the package level, and the only useful class exposed in this package.

#### define_tag(name, func)

`define_tag` correlates a tag name with a function which runs on your dataset.

* `name` parameter should be descriptive
* `func` parameter must be callable, and should return a Boolean for consistent results

#### analyze(data = [], purge = False)

`analyze` is used to iterate over new and existing data and assign tags.

Any existing data that has been analyzed will be re-analyzed every time `analyze` is called.
This ensures that any newly defined tags will be analyzed on existing data.

If you want to re-use the same TagSet (and tag definitions) on a new dataset, you can set call `analyze` with `purge = True`, which will initialize the class with an empty dataset before analyzing new data.

* `data` parameter must be iterable
* `purge` parameter can be used to initalize the analyzed dataset to an empty array, before analyze the new data passed to the `analyze` method

#### query(tags = {})

`query` is how you retrieve data from your dataset that matches the tags passed.

* `tags` parameter must be a dictionary with keys corresponding to tags that have already been defined, and Boolean values. When a value is `True`, the dataset will be filtered to only include results where that tag is `True` (present). When a value is `False`, the dataset will be filtered to only include results where that tag is `False` (absent). `tags` can support as many tags in the dictionary as are defined. Omitted tags are allowed to be either `True` (present) or `False` (absent). Therefore, the default argument of an empty dictionary `{}` will return all analyzed data in the dataset.
