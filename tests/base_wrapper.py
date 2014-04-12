import ctypes

from functools import partial

import helpers


# ctypes wrapper
list_lib = helpers.get_lib('list.so')


class __Index(ctypes.Structure):
    pass

_Index = ctypes.POINTER(__Index)


class __Data(ctypes.Structure):
    pass

_Data = ctypes.POINTER(__Data)


class __Pair(ctypes.Structure):
    pass

_Pair = ctypes.POINTER(__Pair)


# index_t index_from_string(char *s)
index_from_string = helpers.wrap_func(
    list_lib.index_from_string, _Index, [ctypes.c_char_p])


# char *index_to_string(index_t index)
index_to_string = partial(
    helpers.str_from_ptr, helpers.wrap_func(
        list_lib.index_to_string, ctypes.c_void_p, [_Index]))


# bool index_is_less_than(index_t index, index_t other)
index_is_less_than = helpers.wrap_func(
    list_lib.index_is_less_than, ctypes.c_bool, [_Index, _Index])


# index_t index_destroy(index_t index)
index_destroy = helpers.wrap_func(list_lib.index_destroy, _Index, [_Index])


# data_t data_from_string(char *s)
data_from_string = helpers.wrap_func(
    list_lib.data_from_string, _Data, [ctypes.c_char_p])


# char *data_to_string(data_t data)
data_to_string = partial(
    helpers.str_from_ptr, helpers.wrap_func(
        list_lib.data_to_string, ctypes.c_void_p, [_Data]))


# data_t data_destroy(data_t data)
data_destroy = helpers.wrap_func(list_lib.data_destroy, _Data, [_Data])


# pair_t pair_from_index_data(index_t k, data_t d)
pair_from_index_data = helpers.wrap_func(
    list_lib.pair_from_index_data, _Pair, [_Index, _Data])


# pair_t pair_destroy(pair_t pair)
pair_destroy = helpers.wrap_func(list_lib.pair_destroy, _Pair, [_Pair])


# pair_t pair_fst(pair_t pair)
pair_fst = helpers.wrap_func(list_lib.pair_fst, _Index, [_Pair])


# pair_t pair_snd(pair_t pair)
pair_snd = helpers.wrap_func(list_lib.pair_snd, _Data, [_Pair])


# bool pair_is_equal(pair_t pair, pair_t other)
pair_is_equal = helpers.wrap_func(
    list_lib.pair_is_equal, ctypes.c_bool, [_Pair, _Pair])


# pair_t pair_copy(pair_t pair)
pair_copy = helpers.wrap_func(list_lib.pair_copy, _Pair, [_Pair])
