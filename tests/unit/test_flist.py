import unittest
import sys
import os
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fpu')))  # noqa
from fp import *  # noqa
from flist import *  # noqa

#####################
# Testing Class
#####################

class GFTestCase(unittest.TestCase):
    r'''
    Test Case(s) of global function(s) from flist.py
    '''
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_api_reduce(self):
        r'''
        Testing API List.reduce
        '''
        alist = fl(2, 4, 6, 8, 10)
        self.assertEqual(30, alist.reduce(lambda a, b: a + b))
        self.assertEqual(31, alist.reduce(lambda a, b: a + b, 1))

    def test_api_foldLeft(self):
        r'''
        Testing API List.foldLeft
        '''
        alist = fl(1, 2, 3, 4, 5)
        self.assertEqual('012345', alist.foldLeft(0, lambda a, e: "{}{}".format(a, e)))
        self.assertEqual(15, alist.foldLeft(0, lambda a, e: a + e))
        self.assertEqual(120.0, alist.foldLeft(1.0, lambda a, e: a * e))

    def test_gapi_fl(self):
        r'''
        Testing global API:fl to create object of List
        '''
        alist = fl(1, 2, 3)
        self.assertEqual('[1, 2, 3, NIL]', str(alist))
        self.assertEqual(3, alist.size()) 
        self.assertEqual(3, alist.length())
        self.assertEqual(1, alist.head())
        self.assertEqual('[2, 3, NIL]', str(alist.tail()))
        
    def test_gapi_concat(self):
        r'''
        Testing global API:concat to concat two list
        '''
        list1 = fl(1, 2, 3)
        list2 = fl(4, 5, 6)
        list3 = concat(list1, list2)
        self.assertEqual('[1, 2, 3, 4, 5, 6, NIL]', str(list3))

    def test_api_exists(self):
        r'''
        Testing List.exists
        '''
        alist = fl(1, 2, 3)
        self.assertTrue(alist.exists(lambda e: e == 1))
        self.assertFalse(alist.exists(lambda e: e == 5))

    def test_api_drop(self):
        r'''
        Testing List.drop
        '''
        alist = fl(1, 2, 3, 4, 5)
        nlist = alist.drop(3)
        self.assertEqual('[4, 5, NIL]', str(nlist))

    def test_api_dropWhile(self):
        r'''
        Testing List.dropWhile
        ''' 
        alist = fl(range(10)).reverse()  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, NIL]
        nlist = alist.dropWhile(lambda e: e < 5)
        self.assertEqual('[5, 6, 7, 8, 9, NIL]', str(nlist))

    def test_api_init(self):
        r'''
        Testing List.init
        '''
        alist = fl(range(10)).reverse()  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, NIL]
        nlist = alist.init()
        self.assertEqual('[0, 1, 2, 3, 4, 5, 6, 7, 8, NIL]', str(nlist))

    def test_api_filter(self):
        r'''
        Testing List.filter
        '''
        alist = fl(range(10)).reverse()  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, NIL]
        nlist = alist.filter(lambda e: e % 2 == 0)
        self.assertEqual('[0, 2, 4, 6, 8, NIL]', str(nlist))

    def test_api_map(self):
        r'''
        Testing List.map
        '''
        alist = fl(1, 2, 3)
        nlist = alist.map(lambda e: e * 2)
        self.assertEqual('[2, 4, 6, NIL]', str(nlist))

    def test_api_flatMap(self):
        r'''
        Testing List.flatMap
        '''
        alist = fl(1, 2, 3)
        nlist = alist.flatMap(lambda e: fl(e, e * 2))
        self.assertEqual('[1, 2, 2, 4, 3, 6, NIL]', str(nlist))

    def test_uapi_fsum(self):
        r'''
        Testing utility function fsum
        ''' 
        alist = fl(range(10))
        self.assertEqual(45, fsum(alist))
        self.assertEqual(0, fsum(fl()))

    def test_uapi_fproduct(self):
        r'''
        Testing utility function fproduct
        '''
        alist = fl(1, 2, 3)
        self.assertEqual(6.0, fproduct(alist))
        self.assertEqual(1.0, fproduct(fl()))

    def test_uapi_flatten(self):
        r'''
        Testing utility function flatten
        '''
        alist = fl()
        alist = alist.cons(fl(4, 5, 6))
        alist = alist.cons(fl(1, 2, 3))
        self.assertEqual('[[1, 2, 3, NIL], [4, 5, 6, NIL], NIL]', str(alist))
        nlist = flatten(alist)
        self.assertEqual('[1, 2, 3, 4, 5, 6, NIL]', str(nlist))

    def test_feat_forin(self):
        alist = fl(1, 2, 3)
        i = 1
        for e in alist:
            self.assertEqual(i, e)
            i += 1
