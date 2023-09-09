import unittest
import sys
import os
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fpu')))  # noqa
from fp import *  # noqa
import flist
from flist import *  # noqa


#####################
# Testing Class
#####################


class ListTest(unittest.TestCase):
  """Unit test cases of interfact List."""

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_method_sum(self):
    raw_data = [1, 2, 3, 4]
    fpu_list = fl(*raw_data)

    sum_result = fpu_list.sum()

    self.assertEqual(sum_result, sum(raw_data))

  def test_method_zip(self):
    raw_data = ['abc', '123', 'def']
    fpu_list = fl(*raw_data)

    fpu_zip_list = fpu_list.zip()

    self.assertTrue(isinstance(fpu_zip_list, flist.List))
    self.assertEqual(
        list(fpu_zip_list),
        [('a', '1', 'd'), ('b', '2', 'e'), ('c', '3', 'f')])


class GFTestCase(unittest.TestCase):
  """Test Case(s) of global function(s) from module `flist`"""
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_api_reduce(self):
    """Testing API List.reduce."""
    alist = fl(2, 4, 6, 8, 10)
    self.assertEqual(30, alist.reduce(lambda a, b: a + b))
    self.assertEqual(31, alist.reduce(lambda a, b: a + b, 1))

  def test_api_foldLeft(self):
    """Testing API List.foldLeft."""
    alist = fl(1, 2, 3, 4, 5)
    self.assertEqual('012345', alist.foldLeft(0, lambda a, e: "{}{}".format(a, e)))
    self.assertEqual(15, alist.foldLeft(0, lambda a, e: a + e))
    self.assertEqual(120.0, alist.foldLeft(1.0, lambda a, e: a * e))

  def test_api_foldLeft_with_short_stop(self):
    alist = fl(1, 2, 3, 4, 5)

    result = alist.foldLeft(
        0, lambda a, b: a + b,
        short_stop_func=lambda v: v > 3)

    # The folding operation will stop at element 4.
    # So we have folding result as 0 + 1 + 2 + 3 = 6
    self.assertEqual(result, 6)

  def test_gapi_fl(self):
    """Testing global API:fl to create object of List."""
    alist = fl(1, 2, 3)
    self.assertEqual('[1, 2, 3, NIL]', str(alist))
    self.assertEqual(3, alist.size())
    self.assertEqual(3, alist.length())
    self.assertEqual(1, alist.head())
    self.assertEqual('[2, 3, NIL]', str(alist.tail()))

  def test_gapi_comp(self):
    """Testing global API:comp to generate composition from given list."""
    # Composition for 2 element of [1, 2, 3] will be [(1, 2), (1, 3), (2, 3)]
    fpu_comp_list = comp([1, 2, 3], 2)

    self.assertEqual('[(1, 2), (1, 3), (2, 3), NIL]', str(fpu_comp_list))

  def test_gapi_concat(self):
    """Testing global API:concat to concat two list."""
    list1 = fl(1, 2, 3)
    list2 = fl(4, 5, 6)
    list3 = concat(list1, list2)
    self.assertEqual('[1, 2, 3, 4, 5, 6, NIL]', str(list3))

  def test_api_exists(self):
    """Testing List.exists."""
    alist = fl(1, 2, 3)
    self.assertTrue(alist.exists(lambda e: e == 1))
    self.assertFalse(alist.exists(lambda e: e == 5))

  def test_api_drop(self):
    """Testing List.drop."""
    alist = fl(1, 2, 3, 4, 5)
    nlist = alist.drop(3)
    self.assertEqual('[4, 5, NIL]', str(nlist))

  def test_api_dropWhile(self):
    """Testing List.dropWhile."""
    alist = fl(range(10)).reverse()  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, NIL]
    nlist = alist.dropWhile(lambda e: e < 5)
    self.assertEqual('[5, 6, 7, 8, 9, NIL]', str(nlist))

  def test_api_init(self):
    """Testing List.init."""
    alist = fl(range(10)).reverse()  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, NIL]
    nlist = alist.init()
    self.assertEqual('[0, 1, 2, 3, 4, 5, 6, 7, 8, NIL]', str(nlist))

  def test_api_filter(self):
    """Testing List.filter."""
    alist = fl(range(10)).reverse()  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, NIL]
    nlist = alist.filter(lambda e: e % 2 == 0)
    self.assertEqual('[0, 2, 4, 6, 8, NIL]', str(nlist))

  def test_api_map(self):
    """Testing List.map."""
    alist = fl(1, 2, 3)
    nlist = alist.map(lambda e: e * 2)
    self.assertEqual('[2, 4, 6, NIL]', str(nlist))

  def test_api_flatMap(self):
    """Testing List.flatMap."""
    alist = fl(1, 2, 3)
    nlist = alist.flatMap(lambda e: fl(e, e * 2))
    self.assertEqual('[1, 2, 2, 4, 3, 6, NIL]', str(nlist))

  def test_uapi_fsum(self):
    """Testing utility function fsum."""
    alist = fl(range(10))
    self.assertEqual(45, fsum(alist))
    self.assertEqual(0, fsum(fl()))

  def test_uapi_fproduct(self):
    """Testing utility function fproduct."""
    alist = fl(1, 2, 3)
    self.assertEqual(6.0, fproduct(alist))
    self.assertEqual(1.0, fproduct(fl()))

  def test_uapi_flatten(self):
    """Testing utility function flatten."""
    alist = fl()
    alist = alist.cons(fl(4, 5, 6))
    alist = alist.cons(fl(1, 2, 3))
    self.assertEqual('[[1, 2, 3, NIL], [4, 5, 6, NIL], NIL]', str(alist))
    nlist = flatten(alist)
    self.assertEqual('[1, 2, 3, 4, 5, 6, NIL]', str(nlist))

  def test_feat_for_in(self):
    """Testing iteration."""
    alist = fl(1, 2, 3)
    i = 1
    for e in alist:
      self.assertEqual(i, e)
      i += 1
