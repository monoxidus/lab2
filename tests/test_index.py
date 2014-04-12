from unittest import TestCase

from base_wrapper import (
    index_destroy,
    index_from_string,
    index_is_less_than,
    index_to_string,
)


class IndexTestCase(TestCase):

    def setUp(self):
        super(IndexTestCase, self).setUp()
        self.instance = self.new_index("foo")

    def new_index(self, text):
        i = index_from_string(text)
        self.addCleanup(index_destroy, i)
        return i

    def assert_is_less_than(self, expected, i1, i2):
        if index_is_less_than(i1, i2) != expected:
            extra = '' if expected else ' not'
            self.fail('The index %r should %sbe less than %r.' %
                      (index_to_string(i1), extra, index_to_string(i2)))

    def test_same_instance_is_not_less_than_itself(self):
        self.assert_is_less_than(False, self.instance, self.instance)

    def test_aaaa_is_less_than_ab(self):
        self.assert_is_less_than(True, self.new_index("aaaa"),
                                 self.new_index("ab"))

    def test_foo_is_less_than_fooo(self):
        self.assert_is_less_than(True, self.instance, self.new_index("fooo"))

    def test_foo_is_not_less_than_empty_string(self):
        self.assert_is_less_than(False, self.instance, self.new_index(""))

    def test_is_less_than_works_with_non_chars(self):
        self.assert_is_less_than(True, self.new_index("___"), self.instance)

    def test_is_less_than_is_case_sensitive(self):
        self.assert_is_less_than(True, self.new_index("A"),
                                 self.new_index("a"))
