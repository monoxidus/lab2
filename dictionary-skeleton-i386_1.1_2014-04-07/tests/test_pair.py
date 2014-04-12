from unittest import TestCase

from base_wrapper import (
    index_from_string,
    index_to_string,
    data_from_string,
    data_to_string,
    pair_copy,
    pair_destroy,
    pair_from_index_data,
    pair_fst,
    pair_is_equal,
    pair_snd,
)


class PairTestCase(TestCase):

    def new_pair(self, key, value):
        i = index_from_string(key)
        d = data_from_string(value)
        p = pair_from_index_data(i, d)
        self.addCleanup(pair_destroy, p)
        return p

    def test_fst(self):
        i = 'heaven'
        d = 'knocking on its doors'
        p = self.new_pair(i, d)

        self.assertEqual(data_to_string(pair_snd(p)), d)

    def test_snd(self):
        i = 'heaven'
        d = 'knocking on its doors'
        p = self.new_pair(i, d)

        self.assertEqual(data_to_string(pair_snd(p)), d)

    def test_is_equal_empty_index_and_empty_data(self):
        p1 = self.new_pair('', '')
        p2 = self.new_pair('', '')

        self.assertEqual(pair_is_equal(p1, p2), True)

    def test_is_equal_non_empty_index_and_empty_data(self):
        p1 = self.new_pair('foo', '')
        p2 = self.new_pair('foo', '')

        self.assertEqual(pair_is_equal(p1, p2), True)

    def test_is_equal_non_empty_index_and_non_empty_data(self):
        p1 = self.new_pair('foo', 'bar')
        p2 = self.new_pair('foo', 'bar')

        self.assertEqual(pair_is_equal(p1, p2), True)

    def test_is_not_equal_other_empty_index_and_empty_data(self):
        p1 = self.new_pair('foo', 'bar')
        p2 = self.new_pair('', '')

        self.assertEqual(pair_is_equal(p1, p2), False)

    def test_is_not_equal_other_same_index_and_empty_data(self):
        p1 = self.new_pair('foo', 'bar')
        p2 = self.new_pair('foo', '')

        self.assertEqual(pair_is_equal(p1, p2), False)

    def test_is_not_equal_other_same_index_and_different_data(self):
        p1 = self.new_pair('foo', 'bar')
        p2 = self.new_pair('foo', 'ba')

        self.assertEqual(pair_is_equal(p1, p2), False)

    def test_is_not_equal_other_different_index_and_same_data(self):
        p1 = self.new_pair('foo', 'bar')
        p2 = self.new_pair('fooo', 'bar')

        self.assertEqual(pair_is_equal(p1, p2), False)

    def test_is_not_equal_other_both_different(self):
        p1 = self.new_pair('foo', 'barr')
        p2 = self.new_pair('fooo', 'bar')

        self.assertEqual(pair_is_equal(p1, p2), False)
