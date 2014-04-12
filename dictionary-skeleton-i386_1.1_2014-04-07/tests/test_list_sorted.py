from helpers import skip_if_not_implemented
from test_list import BaseTestCase


class SortedListTestCase(BaseTestCase):

    @skip_if_not_implemented
    def test_add(self):
        elems = [
            ('foo', 'zaraza'),
            ('foo', 'zaraza'),
            ('zarara', 'not important'),
            ('xilofon', 'not important'),
            ('medianera', 'not important'),
            ('foo', 'zaraza'),
            ('arb', 'not important'),
            ('arbol', 'not important'),
            ('arbo', 'not important'),
            ('foo', 'zaraza'),
        ]
        for i, d in elems:
            self.instance.add(i, d)

        # ideally we should use cleaner ways of checking the list,
        # but for that we'd need to force either index, or implementing
        # iterable functionality
        elems.sort()  # sort!
        self.assertEqual(self.instance.to_list(), elems)
