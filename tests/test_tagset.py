import unittest
from datatag import TagSet
from datatag.exceptions import TagNotUnique, ArgumentNotCallable, DataNotIterable, UndefinedTag, NonBooleanQueryValue
from datatag.tag_definition import TagDefinition

class TestDefineTag(unittest.TestCase):
    def setUp(self):
        self.ts = TagSet()

    def test_duplicate_name(self):
        self.ts.define_tag('test_tag', lambda x: True)
        self.assertRaises(TagNotUnique, self.ts.define_tag, 'test_tag', lambda x: True)

    def test_function_not_callable(self):
        self.assertRaises(ArgumentNotCallable, self.ts.define_tag, 'test_tag', True)

    def test_adds_tag_definition(self):
        self.ts.define_tag('test_tag', lambda x: True)
        self.assertIn('test_tag', self.ts.tag_definitions)

    def test_adds_correct_type(self):
        self.ts.define_tag('test_tag', lambda x: True)
        self.assertIsInstance(self.ts.tag_definitions['test_tag'], TagDefinition)

    def test_increments_integer(self):
        self.ts.define_tag('tag1', lambda x: True)
        self.ts.define_tag('tag2', lambda x: True)
        self.ts.define_tag('tag3', lambda x: True)
        self.assertEqual(self.ts.tag_definitions['tag1'].flag, 1 << 0)
        self.assertEqual(self.ts.tag_definitions['tag2'].flag, 1 << 1)
        self.assertEqual(self.ts.tag_definitions['tag3'].flag, 1 << 2)

class TestIsIncluded(unittest.TestCase):
    def setUp(self):
        self.ts = TagSet()
        # set up bitflags for fake "tags" that data might have
        self.blue = 1 << 0
        self.red = 1 << 1
        self.green = 1 << 2
        self.orange = 1 << 4

    def test_positive_included_negative_excluded(self):
        # item is blue AND red, not green or orange
        test_data_mask = self.blue + self.red
        positive = self.blue
        negative = self.green
        # apparently this is the syntax for calling private methods...
        result = self.ts._TagSet__is_included(test_data_mask, positive, negative)
        self.assertEqual(result, True)

    def test_multiple_positive_included_multiple_negative_excluded(self):
        # item is blue AND red, not green or orange
        test_data_mask = self.blue + self.red
        positive = self.blue + self.red
        negative = self.green + self.orange
        result = self.ts._TagSet__is_included(test_data_mask, positive, negative)
        self.assertEqual(result, True)

    def test_positive_included_negative_included(self):
        # item is blue AND red, not green or orange
        test_data_mask = self.blue + self.red
        positive = self.blue
        negative = self.red
        result = self.ts._TagSet__is_included(test_data_mask, positive, negative)
        self.assertEqual(result, False)

    def test_positive_included_multiple_negative_included(self):
        # item is blue AND red, not green or orange
        test_data_mask = self.blue + self.red
        positive = self.blue
        negative = self.red + self.green
        result = self.ts._TagSet__is_included(test_data_mask, positive, negative)
        self.assertEqual(result, False)

    def test_positive_excluded_negative_included(self):
        # item is blue AND red, not green or orange
        test_data_mask = self.blue + self.red
        positive = self.green
        negative = self.red
        result = self.ts._TagSet__is_included(test_data_mask, positive, negative)
        self.assertEqual(result, False)

    def test_positive_excluded_negative_excluded(self):
        # item is blue AND red, not green or orange
        test_data_mask = self.blue + self.red
        positive = self.green
        negative = self.orange
        result = self.ts._TagSet__is_included(test_data_mask, positive, negative)
        self.assertEqual(result, False)

    def test_multiple_positive_excluded_multiple_negative_excluded(self):
        # item is blue AND red, not green or orange
        test_data_mask = self.blue + self.red
        positive = self.green + self.blue
        negative = self.orange + self.red
        result = self.ts._TagSet__is_included(test_data_mask, positive, negative)
        self.assertEqual(result, False)


class TestAnalyze(unittest.TestCase):
    def setUp(self):
        self.ts = TagSet()

    def test_data_not_iterable(self):
        data = 23
        self.assertRaises(DataNotIterable, self.ts.analyze, data)
    
    def test_purge_clears_dataset(self):
        data = [1, 2, 3]
        self.ts.analyze(data)
        new_data = [4, 5, 6]
        self.ts.analyze(new_data, purge = True)
        self.assertEqual([datum.value for datum in self.ts.dataset], new_data)

    def test_analyze_all_data(self):
        data = [2, 4, 5, 7, 8]
        self.ts.define_tag('even', lambda x: x % 2 == 0)
        self.ts.analyze(data)
        # bitmask for TaggedDatum should be 1 (1<<0) for data that _is_ even, and 0 for data that is _not_ even
        self.assertEqual([d.value for d in self.ts.dataset if d.bitmask == 1], [2, 4, 8])
        self.assertEqual([d.value for d in self.ts.dataset if d.bitmask == 0], [5, 7])
        self.assertEqual(len(self.ts.dataset), len(data))

class TestQuery(unittest.TestCase):
    def setUp(self):
        self.ts = TagSet()
        self.ts.define_tag('blue', lambda x: 'blue' in x)
        self.ts.define_tag('red', lambda x: 'red' in x)
        self.ts.define_tag('green', lambda x: 'green' in x)
        self.ts.define_tag('orange', lambda x: 'orange' in x)
        data = ['blue', 'red', 'green', 'orange',
                'blue_red', 'blue_green', 'blue_orange',
                'red_green', 'red_orange',
                'green_orange',
                'blue2', 'blue_green_2',
                'blue_red_green_orange']
        self.ts.analyze(data)

    def test_query_for_undefined_tag(self):
        self.assertRaises(UndefinedTag, self.ts.query, {'undefined_tag': True})

    def test_query_for_non_boolean_value(self):
        self.ts.define_tag('tag1', lambda x: True)
        self.assertRaises(NonBooleanQueryValue, self.ts.query, {'tag1': "True"})
        
    def test_finds_data_single_positive_param(self):
        params = {'blue': True}
        actual = self.ts.query(params)
        expected = ['blue', 'blue_red', 'blue_green', 'blue_orange', 'blue2', 'blue_green_2', 'blue_red_green_orange']
        self.assertEqual(actual, expected)

    def test_finds_data_single_negative_param(self):
        params = {'blue': False}
        actual = self.ts.query(params)
        expected = ['red', 'green', 'orange', 'red_green', 'red_orange', 'green_orange']
        self.assertEqual(actual, expected)

    def test_finds_data_multiple_positive_param(self):
        params = {'blue': True, 'green': True}
        actual = self.ts.query(params)
        expected = ['blue_green', 'blue_green_2', 'blue_red_green_orange']
        self.assertEqual(actual, expected)

    def test_finds_data_multiple_negative_param(self):
        params = {'blue': False, 'green': False}
        actual = self.ts.query(params)
        expected = ['red', 'orange', 'red_orange']
        self.assertEqual(actual, expected)

    def test_finds_data_single_positive_single_negative_param(self):
        params = {'red': True, 'green': False}
        actual = self.ts.query(params)
        expected = ['red', 'blue_red', 'red_orange']
        self.assertEqual(actual, expected)

    def test_finds_data_multiple_positive_multiple_negative_param(self):
        params = {'red': True, 'blue': True, 'green': False, 'orange': False}
        actual = self.ts.query(params)
        expected = ['blue_red']
        self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()