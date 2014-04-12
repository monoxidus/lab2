import ctypes
import os
import tempfile

from functools import partial

import helpers


# ctypes wrapper
dict_lib = helpers.get_lib('dict.so')


# TADs

class __Dictionary(ctypes.Structure):
    pass


_Dictionary = ctypes.POINTER(__Dictionary)
_Word = ctypes.c_char_p
_Definition = ctypes.c_char_p


# Wrappers

# dict_t dict_empty(void)
dict_empty = helpers.maybe_implemented(
    dict_lib, 'dict_empty', _Dictionary, [])


# dict_t dict_destroy(dict_t dict)
dict_destroy = helpers.maybe_implemented(
    dict_lib, 'dict_destroy', _Dictionary, [_Dictionary])


# unsigned int dict_length(dict_t dict)
dict_length = helpers.maybe_implemented(
    dict_lib, 'dict_length', ctypes.c_uint, [_Dictionary])


# bool dict_is_equal(dict_t dict, dict_t other)
dict_is_equal = helpers.maybe_implemented(
    dict_lib, 'dict_is_equal', ctypes.c_bool, [_Dictionary, _Dictionary])


# bool dict_exists(dict_t dict, word_t word)
dict_exists = helpers.maybe_implemented(
    dict_lib, 'dict_exists', ctypes.c_bool, [_Dictionary, _Word])


# char *data_to_string(data_t data)
dict_search = partial(
    helpers.str_from_ptr, helpers.wrap_func(
        dict_lib.dict_search, ctypes.c_void_p, [_Dictionary, _Word]))


# dict_t dict_add(dict_t dict, word_t word, def_t def)
dict_add = helpers.maybe_implemented(
    dict_lib, 'dict_add', _Dictionary, [_Dictionary, _Word, _Definition])


# dict_t dict_remove(dict_t dict, word_t word)
dict_remove = helpers.maybe_implemented(
    dict_lib, 'dict_remove', _Dictionary, [_Dictionary, _Word])


# dict_t dict_copy(dict_t dict)
dict_copy = helpers.maybe_implemented(
    dict_lib, 'dict_copy', _Dictionary, [_Dictionary])


# void dict_dump(dict_t dict, FILE *fd)
dict_dump = helpers.maybe_implemented(
    dict_lib, 'dict_dump', None, [_Dictionary, helpers.FILE_ptr])


def create_string_buffer(value):
    if isinstance(value, basestring):
        value = ctypes.create_string_buffer(value)

    return value


class Dictionary(dict):

    def __init__(self, iterable=None):
        self._d = dict_empty()

    def __del__(self):
        self._d = dict_destroy(self._d)

    def __contains__(self, k):
        k = create_string_buffer(k)
        return dict_exists(self._d, k)

    def __iter__(self):
        raise NotImplementedError()

    def __delitem__(self, k):
        k = create_string_buffer(k)
        dict_remove(self._d, k)

    def __getitem__(self, k):
        k = create_string_buffer(k)
        return dict_search(self._d, k)

    def __setitem__(self, k, v):
        k = create_string_buffer(k)
        v = create_string_buffer(v)
        self._d = dict_add(self._d, k, v)

    def __len__(self):
        return dict_length(self._d)

    def __eq__(self, other):
        return (isinstance(other, Dictionary) and
                dict_is_equal(self._d, other._d))

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        fd, tmp = tempfile.mkstemp()
        fd = os.fdopen(fd, 'r+')

        self.dump(fd)
        fd.seek(0)
        result = fd.read()
        fd.close()

        os.remove(tmp)
        return result

    def __repr__(self):
        return repr(self.to_dict())

    def dump(self, fd):
        dict_dump(self._d, helpers.get_file_ptr(fd))

    def clear(self):
        dict_destroy(self._d)
        self._d = dict_empty()

    def copy(self):
        result = Dictionary()
        dict_destroy(result._d)
        result._d = dict_copy(self._d)
        return result

    def fromkeys(self, keys, values):
        assert len(keys) == len(values)
        for k, v in zip(keys, values):
            self[k] = v

    def to_dict(self):
        result = str(self).strip().strip('}').strip('{').strip()
        if result:
            # split per \n
            result = dict(map(str.strip, line.split(':', 1))
                          for line in result.split('\n'))
        else:
            result = {}
        return result
