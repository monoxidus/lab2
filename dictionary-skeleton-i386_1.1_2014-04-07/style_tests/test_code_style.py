from unittest import TestCase

from helpers import IndentMixinTestCase


class MainIndentTestCase(TestCase, IndentMixinTestCase):
    filenames = ('main.c',)


class DictIndentTestCase(TestCase, IndentMixinTestCase):
    filenames = ('dict.c',)


###class IndexIndentTestCase(TestCase, IndentMixinTestCase):
###    filenames = ('index.c',)


###class PairIndentTestCase(TestCase, IndentMixinTestCase):
###    filenames = ('pair.c',)


###class ListIndentTestCase(TestCase, IndentMixinTestCase):
###    filenames = ('list.c',)
