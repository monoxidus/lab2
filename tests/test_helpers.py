from unittest import TestCase

from helpers import uint_string_list_to_list


class StringListToListTestCase(TestCase):

    def test_empty_string(self):
        result = uint_string_list_to_list('')
        self.assertEqual(result, [])

    def test_empty_list(self):
        result = uint_string_list_to_list('[]')
        self.assertEqual(result, [])

    def test_empty_list_with_spaces(self):
        result = uint_string_list_to_list('   \n  [   \n \t  ]  \n\n   \t')
        self.assertEqual(result, [])

    def test_empty_tuples(self):
        result = uint_string_list_to_list('[(), ()]')
        self.assertEqual(result, [(), ()])

    def test_not_empty_tuples(self):
        result = uint_string_list_to_list('[(2, 3),(5,6), 9,(5, 852, 100)]')
        self.assertEqual(result, [(2, 3), (5, 6), 9, (5, 852, 100)])
