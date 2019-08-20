# TODO: how to export TraitSet directly from `inclusion` package...?
from inclusion.traitset import TraitSet

# helper methods to assist with printing
def title(string):
    print("###################")
    print("#")
    print("# {}".format(string))
    print("#")
    print("###################")
    print("")

def print_results(params):
    print("Query params: {}".format(params))
    print("Results: {}\n".format(traitset.query(params)))




# instantiate our TraitSet
traitset = TraitSet()




# define some traits for our TraitSet.
# In this example we have two traits:
#   `has_an_e` will be True any data that contains an 'e'
#   `greater_than_3_chars` will be True for any data that has more than 3 characters
#
# Note that traits can be defined with either a lambda or a function
def greater_than_three_chars(datum):
    return len(datum) > 3

traitset.define_trait('has_an_e', lambda d: 'e' in d.lower())
traitset.define_trait('greater_than_3_chars', greater_than_three_chars)




# create our fake dataset. In this case we use words
paragraph = "Lorem ipsum dolor amet leggings tie chillwave vinyl go"
words = paragraph.split(' ')




# analyze our dataset.
# This step is required before we can query for matching data
traitset.analyze(words)





title("For demonstration, print all combinations and results")

# define the parameters by which we want to search
params = {
    'has_an_e': True,
    'greater_than_3_chars': True
}

print_results(params)
# => Results: ['Lorem', 'amet', 'leggings', 'chillwave']

print_results({'has_an_e': True, 'greater_than_3_chars': False})
# => Results: ['tie']

print_results({'has_an_e': False, 'greater_than_3_chars': True})
# => Results: ['ipsum', 'dolor', 'vinyl']

print_results({'has_an_e': False, 'greater_than_3_chars': False})
# => Results: ['go']






title("By default, `analyze` will append data to the existing dataset")
extra_words = ['on', 'to']
traitset.analyze(extra_words)
print_results({'has_an_e': False, 'greater_than_3_chars': False})
# => Results: ['go', 'on', 'to']





title("If we want to analyze a fresh dataset, we can purge the existing data from our TraitSet")
extra_words = ['on', 'to']
traitset.analyze(extra_words, purge = True)
print_results({'has_an_e': False, 'greater_than_3_chars': False})
# => Results: ['on', 'to']

print_results({'has_an_e': True, 'greater_than_3_chars': False})
# => Results: []





title("Note: omitted parameters are ignored, meaning they are allowed to be either True or False")
new_words = ['fresh', 'me', 'frish', 'mi']
traitset.analyze(new_words, purge = True)
print_results({'has_an_e': True})
# => Results: ['fresh', 'me']

print_results({'greater_than_3_chars': True})
# => Results: ['fresh', 'frish']
