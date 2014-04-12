from unittest import TestCase, SkipTest

from helpers import random_string
from dict_wrapper import Dictionary, create_string_buffer


class DictionaryTestCase(TestCase):

    maxDiff = None

    def setUp(self):
        super(DictionaryTestCase, self).setUp()
        self.instance = Dictionary()

    def keys(self):
        return [random_string(length=10) for i in xrange(10)]

    def values(self):
        return [random_string(length=50, with_spaces=True) for i in xrange(10)]

    def add_some_values(self):
        for k, v in (
            ('perro', 'animal que ladra'), ('gato', 'animal que maulla')):
            self.instance[k] = v

    def test_size_on_empty(self):
        self.instance['foo'] = 'something'
        self.assertEqual(len(self.instance), 1)

    def test_size_on_non_empty(self):
        self.assertEqual(len(self.instance), 0)

    def test_exists_on_empty(self):
        self.assertNotIn('foo', self.instance)

    def test_exists_on_non_empty(self):
        self.assertNotIn('foo', self.instance)

        self.instance['foo'] = 'something'

        self.assertIn('foo', self.instance)

    def test_add_to_empty_dict(self):
        word = 'test'
        definition = 'this is a test'

        self.instance[word] = definition

        self.assertEqual(len(self.instance), 1)
        self.assertEqual(self.instance[word], definition)

    def test_add_to_non_empty_dict(self):
        self.add_some_values()

        word = 'test'
        definition = 'this is a test'

        self.instance[word] = definition

        self.assertEqual(len(self.instance), 3)
        self.assertEqual(self.instance[word], definition)

    def test_remove_only_value(self):
        self.instance['foo'] = 'something'

        del self.instance['foo']

        self.assertNotIn('foo', self.instance)
        self.assertEqual(len(self.instance), 0)

    def test_remove_with_other_values(self):
        self.add_some_values()
        self.instance['foo'] = 'something'

        del self.instance['foo']

        self.assertNotIn('foo', self.instance)
        self.assertEqual(len(self.instance), 2)

    def test_remove_all_values(self):
        keys = self.keys()
        values = self.values()

        self.instance.fromkeys(
            keys=[create_string_buffer(k) for k in keys],
            values=[create_string_buffer(v) for v in values])

        for k in keys:
            del self.instance[k]

        self.assertEqual(len(self.instance), 0)

    def test_is_equal_empty(self):
        other = Dictionary()
        self.assertEqual(self.instance, other)

    def test_is_equal_not_empty(self):
        keys = self.keys()
        values = self.values()

        self.instance.fromkeys(
            keys=[create_string_buffer(k) for k in keys],
            values=[create_string_buffer(v) for v in values])

        other = Dictionary()
        other.fromkeys(
            keys=[create_string_buffer(k) for k in keys],
            values=[create_string_buffer(v) for v in values])

        self.assertEqual(self.instance, other)
        for k, v in zip(keys, values):
            self.assertIn(k, self.instance)
            self.assertIn(k, other)
            self.assertEqual(self.instance[k], other[k])

    def test_copy_empty(self):
        other = self.instance.copy()

        self.assertEqual(self.instance, other)

    def test_copy(self):
        self.instance['foo'] = 'zaraza'
        self.instance['bar'] = 'lorem ipsum sir amet'

        other = self.instance.copy()

        self.assertEqual(self.instance, other)

    def test_to_dict(self):
        keys = self.keys()
        values = self.values()

        self.instance.fromkeys(
            keys=[create_string_buffer(k) for k in keys],
            values=[create_string_buffer(v) for v in values])

        self.assertEqual(
            self.instance.to_dict(), dict(zip(keys, values)))
