import unittest
import random
from fpu.fp import *  # noqa
from fpu import flist
from fpu.flist import *  # noqa
from tests.unit import parameterized


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

  def test_api_cumsum(self):
    test_nums = [1, 2, 3]

    cumsum_result = fl(test_nums).cumsum()

    self.assertEqual(str(cumsum_result), '[3, 5, 6, NIL]')

  def test_api_setHead(self):
    """Testing API Cons.setHead."""
    alist = fl(1, 'x', 2)
    alist = alist.setHead('z')
    self.assertEqual(['z', 'x', 2], list(alist))

  def test_api_reduce(self):
    """Testing API List.reduce."""
    alist = fl(2, 4, 6, 8, 10)
    self.assertEqual(30, alist.reduce(lambda a, b: a + b))
    self.assertEqual(31, alist.reduce(lambda a, b: a + b, 1))

  @parameterized.named_parameters(
    dict(
      testcase_name="case 1",
      identity=None,
      use_fold_right=True,
      expected_result="132"),
    dict(
      testcase_name="case 2",
      identity='0',
      use_fold_right=True,
      expected_result="0321"),
  )
  def test_api_reduce_by_fold_right(
    self, testcase_name, identity, use_fold_right, expected_result
  ):
    # case 1: step 1. a='2', b='3' => '32' step 2. a='32', b='1' => '132'
    alist = fl('1', '2', '3')
    result = alist.reduce(
      lambda a, b: f'{b}{a}', identity, use_fold_right=use_fold_right)
    self.assertEqual(expected_result, result)

  def test_api_reduce_as_fl(self):
    alist = fl('1', '2')
    result = alist.reduce(lambda a, b: a + b, as_fl=True)
    self.assertTrue(isinstance(result, Cons))
    self.assertEqual(list(result), ['1', '2'])

  def test_api_foldLeft(self):
    """Testing API List.foldLeft."""
    alist = fl(1, 2, 3, 4, 5)
    self.assertEqual(
      '012345', alist.foldLeft(0, lambda a, e: "{}{}".format(a, e)))
    self.assertEqual(15, alist.foldLeft(0, lambda a, e: a + e))
    self.assertEqual(120.0, alist.foldLeft(1.0, lambda a, e: a * e))

  @parameterized.named_parameters(
    dict(
      testcase_name='fast case',
      short_stop_func=lambda e: e > 3,
      expected_result=6),
    dict(
      testcase_name='corner case',
      short_stop_func=lambda e: e > -1,
      expected_result=Nil())
  )
  def test_api_foldLeft_with_short_stop(
    self, testcase_name, short_stop_func, expected_result
  ):
    """Testing API Cons.foldLeft with arg short_stop_func."""
    alist = fl(1, 2, 3, 4, 5)
    result = alist.foldLeft(0, lambda a, b: a + b, short_stop_func)
    if isinstance(expected_result, Nil):
      self.assertIsInstance(result, Nil)
    else:
      self.assertEqual(expected_result, result)

  def test_api_foldRight(self):
    """Testing API Cons.foldRight."""
    alist = fl(1, 2, 3, 4, 5)
    self.assertEqual(
      '123450', alist.foldRight(0, lambda a, e: "{}{}".format(a, e)))
    self.assertEqual(15, alist.foldRight(0, lambda a, e: a + e))
    self.assertEqual(120.0, alist.foldRight(1.0, lambda a, e: a * e))

  @parameterized.named_parameters(
    dict(
      testcase_name='fast case',
      short_stop_func=lambda e: e > 3,
      expected_result=15),
    dict(
      testcase_name='corner case',
      short_stop_func=lambda e: e > -1,
      expected_result=Nil())
  )
  def test_api_foldRight_with_short_stop(
    self, testcase_name, short_stop_func, expected_result
  ):
    """Testing API Cons.foldRight with arg short_stop_func."""
    alist = fl(1, 2, 3, 4, 5)
    result = alist.foldRight(0, lambda a, b: a + b, short_stop_func)
    if isinstance(expected_result, Nil):
      self.assertIsInstance(result, Nil)
    else:
      self.assertEqual(expected_result, result)

  def test_gapi_fl(self):
    """Testing global API:fl to create object of List."""
    # case input element (int/float/str) + list + Generator
    def even_number_generator(until: int):
      num = 0
      while num <= until:
        yield num
        num += 2
    alist = fl(-1, ['a', 'b', 'c'], -10.2, even_number_generator(6), 'Hi')
    self.assertEqual('[-1, c, b, a, -10.2, 6, 4, 2, 0, Hi, NIL]', str(alist))
    self.assertEqual(10, alist.size())
    self.assertEqual(10, alist.length())
    self.assertEqual(-1, alist.head())
    self.assertEqual('[c, b, a, -10.2, 6, 4, 2, 0, Hi, NIL]', str(alist.tail()))

  def test_gapi_fl_with_enumerate(self):
    """Testing global API:fl with input as enumerate."""
    test_enumerate = enumerate(['a', 'b'])

    fpu_list = fl(test_enumerate)

    self.assertEqual(list(fpu_list), [(1, 'b'), (0, 'a')])

  @parameterized.named_parameters(
    dict(
      testcase_name='no reverse',
      do_reverse=False,
      expected_result=[3, 2, 1]),
    dict(
      testcase_name='do reverse',
      do_reverse=True,
      expected_result=[1, 2, 3]),
  )
  def test_gapi_fl_do_reverse(
      self, testcase_name, do_reverse, expected_result):
    test_nums = [1, 2, 3]

    fpu_list = fl(test_nums, do_reverse=do_reverse)

    self.assertEqual(list(fpu_list), expected_result)

  @parameterized.named_parameters(
    dict(
      testcase_name='no reverse',
      do_reverse=False,
      expected_result=[3, 2, 1]),
    dict(
      testcase_name='do reverse',
      do_reverse=True,
      expected_result=[1, 2, 3]),
  )
  def test_gapi_fl_do_reverse(
      self, testcase_name, do_reverse, expected_result):
    test_nums = [1, 2, 3]

    fpu_list = fl(test_nums, do_reverse=do_reverse)

    self.assertEqual(list(fpu_list), expected_result)

  @parameterized.named_parameters(
    dict(
      testcase_name='fast case',
      comp_list=comp([1, 2, 3], 2),
      expected_result='[(1, 2), (1, 3), (2, 3), NIL]'),
    dict(
      testcase_name='corner case',
      comp_list=comp([], random.randint(0, 10)),
      expected_result=Nil())
  )
  def test_gapi_comp(self, testcase_name, comp_list, expected_result):
    """Testing global API:comp to generate composition from given list."""
    # fast case: 2-ele-composition of [1, 2, 3] will be [(1, 2), (1, 3), (2, 3)]
    if isinstance(expected_result, Nil):
      self.assertIsInstance(comp_list, Nil)
    else:
      self.assertEqual(expected_result, str(comp_list))

  def test_gapi_concat(self):
    """Testing global API:concat to concat two list."""
    list1 = fl(1, 2, 3)
    list2 = fl(4, 5, 6)
    list3 = concat(list1, list2)
    self.assertEqual('[1, 2, 3, 4, 5, 6, NIL]', str(list3))

  def test_gapi_frange(self):
    """Testing global API:frange to turn range into FPU list."""
    fpu_list = frange(0, 10, 2)

    self.assertEqual('[0, 2, 4, 6, 8, NIL]', str(fpu_list))

  @parameterized.named_parameters(
    dict(
      testcase_name='case 1',
      test_func=lambda e: e == 1,
      expected_result=True),
    dict(
      testcase_name='case 2',
      test_func=lambda e: e == 5,
      expected_result=False),
    dict(
      testcase_name='case 3',
      test_func=lambda e: e > 1,
      expected_result=True),
  )
  def test_api_exists(self, testcase_name, test_func, expected_result):
    """Tests the method `exists` on FPU list."""
    alist = fl(1, 2, 3)

    self.assertEqual(
      alist.exists(test_func), expected_result)

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

  @parameterized.named_parameters(
    dict(
      testcase_name='no initializer',
      test_func=lambda a, b: a + b,
      initializer=None,
      expected_result=[1, 3, 6]),
    dict(
      testcase_name='has initializer',
      test_func=lambda a, b: a + b,
      initializer=10,
      expected_result=[11, 13, 16]),
  )
  def test_api_mapReduce(
      self, testcase_name, test_func, initializer, expected_result):
    """Testing List.mapReduce."""
    test_nums = [1, 2, 3]

    result = list(
        fl(test_nums, do_reverse=True).mapReduce(test_func, initializer))

    self.assertEqual(result, expected_result)

  @parameterized.named_parameters(
    dict(
        testcase_name='FAT',
        test_func=lambda a, b: a + b,
        test_args=[2, 3, 4],
        expected_result=[3, 5, 7]),
    dict(
        testcase_name='shorter_test_args',
        test_func=lambda a, b: a + b,
        test_args=[2, 3],
        expected_result=[3, 5]),
    dict(
        testcase_name='longer_test_args',
        test_func=lambda a, b: a + b,
        test_args=[2, 3, 4, 5],
        expected_result=[3, 5, 7]),
  )
  def test_api_mapWithArgs(
      self, testcase_name, test_func, test_args, expected_result):
    test_nums = [1, 2, 3]

    result = list(
        fl(test_nums, do_reverse=True).mapWithArgs(test_func, test_args))

    self.assertEqual(result, expected_result)

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
    for i, e in enumerate(alist, 1):
      self.assertEqual(i, e)

    alist_iter = iter(alist)
    for i, e in enumerate(alist_iter, 1):
      self.assertEqual(i, e)
    self.assertRaises(StopIteration, alist_iter.next)

  def test_gapi_nil(self):
    """Testing global API:Nil to create object of Nil."""
    nil = Nil()
    self.assertRaises(UOException, nil.head)
    self.assertRaises(UOException, nil.tail)
    self.assertRaises(UOException, nil.setHead, random.random())
    self.assertEqual("[NIL]", str(nil))
    self.assertEqual(nil, nil.drop(random.randint(0, 10)))
    self.assertEqual(nil, nil.dropWhile(lambda e: e in range(10)))
    self.assertEqual(nil, nil.reverse())
    self.assertRaises(UOException, nil.init)
    self.assertRaises(UOException, nil.size)
    self.assertEqual(nil, nil.map(lambda e: e + random.random()))
    self.assertEqual(nil, nil.flatMap(lambda e: fl(e, e * 2)))
    self.assertEqual(nil, nil.filter(lambda e: e % 2 == 0))
    self.assertEqual(None, nil.append(['x', 1, '3']))
    self.assertRaises(UOException, nil.foldRight,
                      identity=-1, f=lambda a, e: "{}{}".format(a, e))
    self.assertRaises(UOException, nil.headOption)
    self.assertEqual(0, nil.sum())
    self.assertEqual(nil, nil.zip())
