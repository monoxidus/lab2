import ctypes
import tempfile
import os

import base_wrapper
import helpers


# ctypes wrapper
list_lib = helpers.get_lib('list.so')


# TADs

class __List(ctypes.Structure):
    pass

_List = ctypes.POINTER(__List)


# list_t list_empty(void)
list_empty = helpers.wrap_func(list_lib.list_empty, _List, [])


# list_t list_destroy(list_t list)
list_destroy = helpers.wrap_func(
    list_lib.list_destroy, _List, [_List])


# unsigned int list_length(list_t list)
list_length = helpers.wrap_func(
    list_lib.list_length, ctypes.c_uint, [_List])


# bool list_is_equal(list_t list, list_t other)
list_is_equal = helpers.wrap_func(
    list_lib.list_is_equal, ctypes.c_bool, [_List, _List])


# data_t list_search(list_t list, index_t index)
list_search = helpers.wrap_func(
    list_lib.list_search, base_wrapper._Data, [_List, base_wrapper._Index])


# list_t list_append(list_t list, index_t index, data_t data)
list_append = helpers.maybe_implemented(
    list_lib, 'list_append', _List,
    [_List, base_wrapper._Index, base_wrapper._Data])


# list_t list_remove(list_t list, index_t index)
list_remove = helpers.wrap_func(
    list_lib.list_remove, _List, [_List, base_wrapper._Index])


# list_t list_copy(list_t list)
list_copy = helpers.wrap_func(
    list_lib.list_copy, _List, [_List])


# void list_dump(list_t list, FILE *fd)
list_dump = helpers.wrap_func(
    list_lib.list_dump, None, [_List, helpers.FILE_ptr])


# Punto estrella 1
# list_t list_add(list_t list, index_t index, data_t data)
list_add = helpers.maybe_implemented(
    list_lib, 'list_add', _List,
    [_List, base_wrapper._Index, base_wrapper._Data])


class List(list):

    def __init__(self):
        self._l = list_empty()

    def __del__(self):
        self._l = list_destroy(self._l)

    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, i):
        raise NotImplementedError()

    def __len__(self):
        return list_length(self._l)

    def __eq__(self, other):
        return isinstance(other, List) and list_is_equal(self._l, other._l)

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
        return repr(self.to_list())

    @classmethod
    def from_linkedlist(cls, linkedlist):
        result = cls()
        result._l = list_destroy(result._l)
        result._l = linkedlist
        return result

    def add(self, i, d):
        i = base_wrapper.index_from_string(i)
        d = base_wrapper.data_from_string(d)
        try:
            self._l = list_add(self._l, i, d)
        except:
            base_wrapper.index_destroy(i)
            base_wrapper.data_destroy(d)
            raise

    def append(self, i, d):
        i = base_wrapper.index_from_string(i)
        d = base_wrapper.data_from_string(d)
        if list_add is not helpers.not_implemented:
            self._l = list_add(self._l, i, d)
        else:
            self._l = list_append(self._l, i, d)

    def copy(self):
        result = List()
        list_destroy(result._l)
        result._l = list_copy(self._l)
        return result

    def count(self, i):
        raise NotImplementedError()

    def dump(self, fd):
        list_dump(self._l, helpers.get_file_ptr(fd))

    def extend(self, other):
        raise NotImplementedError()

    def index(self, i):
        raise NotImplementedError()

    def insert(self, position, pair):
        raise NotImplementedError()

    def pop(self, position=None):
        raise NotImplementedError()

    def remove(self, i):
        i = base_wrapper.index_from_string(i)
        self._l = list_remove(self._l, i)
        base_wrapper.index_destroy(i)

    def reverse(self):
        raise NotImplementedError()

    def search(self, i):
        i = base_wrapper.index_from_string(i)
        d = list_search(self._l, i)
        base_wrapper.index_destroy(i)
        if d:
            return base_wrapper.data_to_string(d)

    def sort(self):
        raise NotImplementedError()

    def to_list(self):
        result = str(self).strip()
        if result:  # split per \n
            result = [tuple(map(str.strip, line.split(':', 1)))
                      for line in result.split('\n')]
        else:
            result = []
        return result
