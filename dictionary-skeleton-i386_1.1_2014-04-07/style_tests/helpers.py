import ast
import ctypes
import difflib
import os
import random
import re
import string
import subprocess

from ctypes.util import find_library
from functools import wraps
from unittest import SkipTest


ALNUM = string.digits + string.letters
LIBC = ctypes.CDLL(find_library('c'))
LIB_DIR = os.path.abspath(os.path.dirname(__file__))


class FILE(ctypes.Structure):
    pass


FILE_ptr = ctypes.POINTER(FILE)
int_ptr = ctypes.POINTER(ctypes.c_int)


def get_lib(filename):
    lib_path = os.path.abspath(os.path.join(LIB_DIR, os.pardir, filename))
    lib = ctypes.CDLL(lib_path)
    return lib


def wrap_func(func, restype, argtypes):
    """Wrap C function setting prototype."""
    func.restype = restype
    func.argtypes = argtypes
    return func


def not_implemented(*a, **kw):
    raise NotImplementedError()


def maybe_implemented(lib, method, *args, **kwargs):
    try:
        result = wrap_func(getattr(lib, method), *args, **kwargs)
    except AttributeError:
        result = None
    if not result:
        result = not_implemented
    return result


def make_int_array_from_iterable(elems):
    array_type = ctypes.c_int * len(elems)
    array = array_type(*elems)
    return array


def make_array_from_iterable(type_in_c, elems):
    """Return a C array of the given type built from the given elems."""
    elems = [e._as_parameter_ if e is not None else type_in_c() for e in elems]
    array_type = type_in_c * len(elems)
    array = array_type(*elems)
    return array


# get a Python string from a char *, freeing the allocated memory
def str_from_ptr(f, ptr, *args):
    if ptr:
        char_pointer = f(ptr, *args)
        result = ctypes.string_at(char_pointer)
        free(char_pointer)
        return result


# stdlib free
free = wrap_func(LIBC.free, None, [ctypes.c_void_p])

# get a file pointer from a python file object
get_file_ptr = wrap_func(
    ctypes.pythonapi.PyFile_AsFile, FILE_ptr, [ctypes.py_object])


def skip_if_not_implemented(f):

    @wraps(f)
    def inner(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
        except NotImplementedError:
            raise SkipTest(
                'PUNTO ESTRELLA: %s is not implemented' % f.__name__)
        return result

    return inner


def random_uint():
    return random.randint(0, 2 ** 16)


def random_string(with_spaces=False, length=10):
    source = ALNUM
    if with_spaces:
        source = ALNUM + ' '
    return ''.join(random.choice(source) for i in xrange(length)).strip()


def uint_string_list_to_list(value, empty=list):
    value = filter(lambda s: not s.isspace(), value)
    try:
        result = ast.literal_eval(value)
    except SyntaxError:
        result = empty()
    return result


class IndentMixinTestCase(object):
    filenames = ()
    COMMAND = ['indent', '-st', '-kr', '-br', '-ce', '-brf', '-ncs',
               '-i4', '-nut', '-l79', '-nbbo', '-pmt', '-cli4']
    DIFFLIB_RE = re.compile(r'href="#difflib_chg_to\d+__0')

    def _generate_html_diff(self, filename):
        command = self.COMMAND + [filename]
        indented = subprocess.check_output(command)
        with open(filename, 'r') as f:
            original = f.readlines()

        differ = difflib.HtmlDiff()
        return differ.make_file(
            original, indented.splitlines(), 'original', 'expected')

    def test_code_style(self):
        style_errors = []
        for f in self.filenames:
            html = self._generate_html_diff(f)
            # if there is at least one diff change, add to list
            if self.DIFFLIB_RE.search(html) is not None:
                style_errors.append(f)
            with open('%s.diff.html' % f, 'w') as output:
                output.write(html)

        if style_errors:
            self.fail(msg="Code style errors: %s" % ', '.join(style_errors))
