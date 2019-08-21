# TODO: how to export TagSet directly from `inclusion` package...?
from datatag import TagSet

# helper methods to assist with printing
def title(string):
    print("###################")
    print("#")
    print("# {}".format(string))
    print("#")
    print("###################")
    print("")

def print_results(params):
    results = tagset.query(params)
    print("Query params: {}".format(params))
    print("Results: {}\n".format(results))
    return results




# instantiate our TagSet
tagset = TagSet()




# define some tags for our TagSet.
# In this example we have two tags:
#   `has_an_e` will be True any data that contains an 'e'
#   `greater_than_3_chars` will be True for any data that has more than 3 characters
#
# Note that tags can be defined with either a lambda or a function
def greater_than_three_chars(datum):
    return len(datum) > 3

tagset.define_tag('has_an_e', lambda d: 'e' in d.lower())
tagset.define_tag('greater_than_3_chars', greater_than_three_chars)




# create our fake dataset. In this case we use words
paragraph = "Lorem ipsum dolor amet leggings tie chillwave vinyl go"
words = paragraph.split(' ')




# analyze our dataset.
# This step is required before we can query for matching data
tagset.analyze(words)





title("For demonstration, print all combinations and results")

# define the parameters by which we want to search
params = {
    'has_an_e': True,
    'greater_than_3_chars': True
}

results = print_results(params)
assert results == ['Lorem', 'amet', 'leggings', 'chillwave']

results = print_results({'has_an_e': True, 'greater_than_3_chars': False})
assert results == ['tie']

results = print_results({'has_an_e': False, 'greater_than_3_chars': True})
assert results == ['ipsum', 'dolor', 'vinyl']

results = print_results({'has_an_e': False, 'greater_than_3_chars': False})
assert results == ['go']






title("By default, `analyze` will append data to the existing dataset")
extra_words = ['on', 'to']
tagset.analyze(extra_words)
results = print_results({'has_an_e': False, 'greater_than_3_chars': False})
assert results == ['go', 'on', 'to']





title("If we want to analyze a fresh dataset, we can purge the existing data from our TagSet")
extra_words = ['on', 'to']
tagset.analyze(extra_words, purge = True)
results = print_results({'has_an_e': False, 'greater_than_3_chars': False})
assert results == ['on', 'to']

results = print_results({'has_an_e': True, 'greater_than_3_chars': False})
assert results == []





title("Note: omitted parameters are ignored, meaning they are allowed to be either True or False")
new_words = ['fresh', 'me', 'squash', 'too']
tagset.analyze(new_words, purge = True)
results = print_results({'has_an_e': True})
assert results == ['fresh', 'me']

results = print_results({'greater_than_3_chars': True})
assert results == ['fresh', 'squash']





title("If you define a new tag after data has already been analyzed, just call analyze again to re-evaluate data")
tagset.define_tag('has_o_or_e', lambda x: 'e' in x or 'o' in x)
tagset.analyze()
results = print_results({'has_o_or_e': True})
assert results == ['fresh', 'me', 'too']




title("You can also analyze complex classes of data instead of base data types. Just adjust your tag definitions accordingly")
class TestClass():
    def __init__(self, name, value):
        self.name = name
        self.value = value

tagset = TagSet()
tagset.define_tag('value_is_true', lambda x: x.value == True)
data = [TestClass('True1', True), TestClass('False1', False), TestClass('True2', True), TestClass('False2', False)]
tagset.analyze(data)
results = print_results({'value_is_true': True})
assert [r.name for r in results] == ['True1', 'True2']
