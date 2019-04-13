import unittest
import sys
import os
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fpu')))  # noqa
# from pprint import pprint
# pprint(sys.path)
from fp import *  # noqa


#####################
# Testing Artifact
#####################
emailPtn = re.compile("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")


class EmailValidationFP:
    def __init__(self):
        self.succEft = self.sendVerificationMail
        self.failEft = self.logError

    def logError(self, msg):
        return 'Error message logged: {}'.format(msg)

    def sendVerificationMail(self, mailAddr):
        return 'Mail sent to {}'.format(mailAddr)

    def validate(self, mailAddr):
        return Case.match(Case.default(Result.success(mailAddr)),
                          Case.mcase(Supplier(lambda s: s is None, mailAddr), Result.failure('Email is None')),
                          Case.mcase(Supplier(lambda s: len(s) == 0, mailAddr), Result.failure('Email is empty')),
                          Case.mcase(Supplier(lambda s: not emailPtn.match(s), mailAddr), Result.failure('Email {} is invalid'.format(mailAddr))))

    def execute(self, mailAddr):
        return self.validate(mailAddr).bind(self.sendVerificationMail, self.logError)


class Product:
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight


class OrderLine:
    def __init__(self, product, count):
        self.product = product
        self.count = count

    def getWeight(self):
        return self.product.weight * self.count

    def getAmount(self):
        return self.product.price * self.count



#####################
# Testing Class
#####################
def sayHi(name):
    return 'Hi {}'.format(name)

def sayBye(name):
    return 'Bye {}'.format(name)

class FPTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gapi_compose2(self):
        def sum2(a, b):
            return a + b
        def double(e):
            return e * 2
        fun = compose2(double, sum2)
        self.assertEqual(fun(1, 2), 6, 'Expect 6')

    def test_gapi_compose(self):
        fun = compose(sayHi, sayBye)
        msg, = fun('John')
        self.assertEqual(msg, 'Hi Bye John')

    def test_gapi_andThen(self):
        fun = andThen(sayHi, sayBye)
        msg = fun('Peter')
        self.assertEqual(msg, 'Bye Hi Peter')

    def test_Supplier(self):
        s = Supplier(lambda s: s+1, 1)
        self.assertEqual(s(), 2, 'Expect 2')

    def test_uc_1(self):
        r'''
        Test user case of Email validation
        '''
        ev = EmailValidationFP()
        self.assertEqual(ev.execute("this.is@my.email"), "Error message logged: Email this.is@my.email is invalid")
        self.assertEqual(ev.execute(None), "Error message logged: Email is None")
        self.assertEqual(ev.execute(""), "Error message logged: Email is empty")
        self.assertEqual(ev.execute("john.doe@acme.com"), "Mail sent to john.doe@acme.com")


class CUTestCase(unittest.TestCase):
    r'''
    Test Cases for class CollectionUtils
    '''
    def setUp(self):
        self.tlist = [1, 2, 3, 4]

    def tearDown(self):
        pass

    def test_crud(self):
        # Creation of list
        alist = CollectionUtils.l(*self.tlist)
        self.assertEqual(len(self.tlist), len(alist))
        for i in range(len(self.tlist)):
            self.assertEqual(self.tlist[i], alist[i])

        alist = CollectionUtils.fl(self.tlist)
        self.assertEqual(len(self.tlist), len(alist))
        for i in range(len(self.tlist)):
            self.assertEqual(self.tlist[i], alist[i])

        olist = CollectionUtils.copy(alist)
        self.assertEqual(len(olist), len(alist))
        for i in range(len(alist)):
            self.assertEqual(alist[i], olist[i])

        # Read of list
        olist = CollectionUtils.head(alist)
        self.assertTrue(len(olist) == 1)
        self.assertTrue(olist[0] == 1)

        olist = CollectionUtils.tail(alist)
        self.assertTrue(len(olist) == (len(alist) - 1))
        for i in range(len(olist)):
            self.assertEqual(olist[i], alist[i+1])

        # Modification/Update of list
        ulist = CollectionUtils.m(alist, lambda e: e + 1)
        self.assertEqual(len(ulist), len(alist))
        for i in range(len(alist)):
            self.assertEqual(ulist[i], alist[i] + 1)

        ulist = CollectionUtils.append(alist, 5)
        self.assertEqual(len(ulist), len(alist)+1)
        self.assertEqual(ulist[-1], 5)

    def test_first(self):
        alist = CollectionUtils.fl(self.tlist)
        olist = CollectionUtils.first(alist, lambda e: e % 2 == 0)
        self.assertTrue(len(olist) == 1, 'Expect to have 1 element (Real={})'.format(len(olist)))
        self.assertTrue(olist[0] == 2, 'Expect to have 2 (Real={})'.format(olist))

    def test_fold(self):
        alist = CollectionUtils.l(*self.tlist)
        rst1 = CollectionUtils.foldLeft(alist, 0, lambda i, e: i + e)
        rst2 = CollectionUtils.foldLeft(alist, 0, lambda e, i: i + e)
        self.assertEqual(rst1, 10)  # 0 + 1 + 2 + 3 + 4 = 10
        self.assertEqual(rst2, 10)  # 0 + 4 + 3 + 2 + 1 = 10

        toothPaste = Product('Tooth paste', 1.5, 0.5)
        toothBrush = Product('Tooth brush', 3.5, 0.3)
        order = CollectionUtils.l(OrderLine(toothPaste, 2),
                                  OrderLine(toothBrush, 3))
        weight = CollectionUtils.foldLeft(order, 0.0, lambda i, e: i + e.getWeight())
        price = CollectionUtils.foldLeft(order, 0.0, lambda i, e: i + e.getAmount())
        self.assertEqual(price, 13.5, 'Expect 13.5 (Real={})'.format(weight))
        self.assertEqual(weight, 1.9, 'Expect 1.9 (Real={})'.format(price))

    def test_revese(self):
        alist = CollectionUtils.l(*self.tlist)
        rlist = CollectionUtils.reverse(alist)
        self.assertTrue(len(alist) == len(rlist))
        for i in range(len(alist)):
            self.assertTrue(alist[i] == rlist[-(i+1)],
                            'i={}; alist[{}]={}; rlist[{}]={}'.format(i, i, alist[i], -(i+1), rlist[-(i+1)]))

    def test_foreach(self):
        alist = CollectionUtils.l(*self.tlist)
        olist = []
        CollectionUtils.forEach(alist, lambda e: olist.append(e + 1))
        self.assertTrue(len(alist) == len(olist))
        for i in range(len(alist)):
            self.assertTrue(alist[i] + 1 == olist[i])

    def test_unfold(self):
        seed = 0
        f = lambda e: e + 1
        p = lambda e: e < 10
        olist = CollectionUtils.unfold(seed, f, p)
        self.assertTrue(len(olist) == 10)
        for i in range(len(olist)):
            self.assertTrue(olist[i] == i)

    def test_range(self):
        # Testing default option
        olist = CollectionUtils.range(0, 10, 1)  # Default is exclusive
        self.assertTrue(len(olist) == 10)
        for i in range(len(olist)):
            self.assertTrue(olist[i] == i)

        # Testing inclusive
        olist = CollectionUtils.range(0, 10, 1, True)
        self.assertTrue(len(olist) == 11)
        for i in range(len(olist)):
            self.assertTrue(olist[i] == i)

class TailCallTest(unittest.TestCase):
    r'''
    Test Cases of class TailCall
    '''
    def setUp(self):
        self.tlist = [1, 2, 3, 4]

    def tearDown(self):
        pass

    def _addRec(self, x, y):
        return TailCall.ret(x) if y == 0 else TailCall.sus(Supplier(self._addRec, x + 1, y - 1))

    def add(self, x, y):
        return self._addRec(x, y).eval()

    def _fibRec(self, n, x, y):
        return TailCall.ret(x) if n == 0 else TailCall.sus(Supplier(self._fibRec, n - 1, y , x + y))

    def fib(self, n, x=0, y=1):
        return self._fibRec(n, x, y).eval()

    def test_add(self):
        self.assertEqual(self.add(3, 10000), 10003)

    def test_fib(self):
        fib_series = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
        for i in range(len(fib_series)):
            self.assertEqual(fib_series[i], self.fib(i))


class OptionTest(unittest.TestCase):
    r'''
    Test Cases of class Option
    '''
    def setUp(self):
        self.tlist = [1, 2, 3, 4]
        self.df = lambda e: e

    def tearDown(self):
        pass

    def test_gapi_some(self):
        someData = 'somedata'
        s = Option.some(someData)
        self.assertTrue(isinstance(s, Some))
        self.assertEqual(someData, s.value)

    def test_gapi_none(self):
        n = Option.none()
        self.assertTrue(isinstance(n, N))        

    def test_api_isSome(self):
        s = Option.some('somedata')
        n = Option.none()
        self.assertTrue(s.isSome())
        self.assertFalse(n.isSome())

    def test_api_getOrElse(self):
        noData = "No data"
        someData = "Some data"
        self.assertEqual(Option.some(someData).getOrElse(Supplier(self.df, noData)), someData)
        self.assertEqual(Option.none().getOrElse(Supplier(self.df, noData)), noData)

    def test_api_getOr(self):
        sValue = "some value"
        dValue = "default value"
        self.assertEqual(sValue, Option.some(sValue).getOr(dValue))
        self.assertEqual(dValue, Option.none().getOr(dValue))

    def test_api_map(self):
        some = Option.some(1)
        none = Option.none()
        double = lambda e: e * 2
        self.assertEqual(Option.some(2), some.map(double))
        self.assertEqual(Option.none(), none.map(double))

    def test_api_flatMap(self):
        some = Option.some(1)
        none = Option.none()
        addOne = lambda e: Option.some(e + 1)
        double = lambda e: Option.some(e * 2)
        self.assertEqual(Option.some(4), some.flatMap(addOne).flatMap(double))
        self.assertEqual(Option.none(), none.flatMap(addOne).flatMap(double))

    def test_api_orElse(self):
        some = Option.some(1)
        none = Option.none()
        def df():
            return Option.some(-1)

        self.assertEqual(Option.some(1), some.orElse(df))
        self.assertEqual(Option.some(-1), none.orElse(df))

    def test_api_filter(self):
        some1 = Option.some(1)
        some2 = Option.some(2)
        none = Option.none()
        bt1 = lambda e: e > 1  # Bigger than one

        self.assertEqual(Option.none(), some1.filter(bt1))
        self.assertEqual(some2, some2.filter(bt1))
        self.assertEqual(none, none.filter(lambda e: e > 1))
