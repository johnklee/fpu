from abc import ABCMeta, abstractmethod
try:
    from fp import *    # noqa
except:                 # noqa
    from .fp import *   # noqa


ret = TailCall.ret      # noqa
sus = TailCall.sus      # noqa


class UOException(Exception):
    r'''
    Unsupported Operation Exception
    '''
    def __init__(self, message, errors=None):
        super(Exception, self).__init__(message)
        self.errors = errors


class List:
    __metaclass__ = ABCMeta

    @abstractmethod
    def head(self):
        raise NotImplementedError()

    @abstractmethod
    def tail(self):
        raise NotImplementedError()

    @abstractmethod
    def isEmpty(self):
        r'''
        * Nil object: False
        * Cons object: True

        @return
            True if Cons object; False otherwise.
        '''
        raise NotImplementedError()

    @abstractmethod
    def setHead(self, h):
        raise NotImplementedError()

    @abstractmethod
    def drop(self, n):
        r'''
        Dropping the n first elements of a list while not mutating or creating anything
        '''
        raise NotImplementedError()

    @abstractmethod
    def dropWhile(self, f):
        r'''
        Method to remove elements from the head of the List as long as a condition holds true.
        '''
        raise NotImplementedError()

    @abstractmethod
    def reverse(self):
        raise NotImplementedError()

    @abstractmethod
    def init(self):
        r'''
        Remove the last element from a list.
        '''
        raise NotImplementedError()

    @abstractmethod
    def size(self):
        raise NotImplementedError()

    @abstractmethod
    def length(self):
        raise NotImplementedError()

    @abstractmethod
    def map(self, f):
        r'''
        Modify each element of a list by applying a specified function to it

        @return
            List object
        '''
        raise NotImplementedError()

    @abstractmethod
    def flatMap(self, f):
        r'''
        method that applies to each element of List<A> a function from A to List<B>, and returns a List<B>

        @return
            List object
        '''
        raise NotImplementedError()

    @abstractmethod
    def filter(self, f):
        r'''
        Method that removes from a list the elements that don't satisfy a given predicate
        '''
        raise NotImplementedError()

    @abstractmethod
    def append(self, e):
        raise NotImplementedError()

    def reduce(self, f, identity=None):
        if identity is not None:
            return self.foldLeft(identity, f)
        else:
            return self.t.foldLeft(self.h, f)

    @abstractmethod
    def foldRight(self, identity, f):
        raise NotImplementedError()

    def foldLeft(self, identity, f):
        return self._foldLeft(identity, self, f).eval()

    def _foldLeft(self, acc, alist, f):
        return ret(acc) if alist.isEmpty() else sus(Supplier(self._foldLeft, f(acc, alist.h), alist.t, f))

    @abstractmethod
    def headOption(self):
        raise NotImplementedError()

    @abstractmethod
    def exists(self, f):
        raise NotImplementedError()

    def cons(self, e):
        return Cons(e, self)

    def __iter__(self):
        return ListIter(self)


class ListIter:
    def __init__(self, cont):
        self.cont = cont

    def __iter__(self):
        return self

    def __next__(self):
        if self.cont.length() == 0:
            raise StopIteration()
        else:
            val = self.cont.head()
            self.cont = self.cont.tail()
            return val

    def next(self):
        return self.__next__()


class Nil(List):
    def __init__(self):
        pass

    def head(self):
        raise UOException('head called on an empty list')

    def tail(self):
        raise UOException('tail called on an empty list')

    def isEmpty(self):
        return True

    def setHead(self, h):
        raise UOException('setHead called on an empty list')

    def __str__(self):
        return "[NIL]"

    def drop(self, n):
        return self

    def dropWhile(self, f):
        return self

    def reverse(self):
        return self

    def init(self):
        raise UOException('init called on an empty list')

    def size(self):
        raise UOException('size called on an empty list')

    def length(self):
        return 0

    def map(self, f):
        return self

    def flatMap(self, f):
        return self

    def filter(self, f):
        return self

    def append(self, a):
        return None

    def foldRight(self, identity, f):
        raise UOException('foldRight called on an empty list')

    def headOption(self):
        raise UOException('headOption called on an empty list')

    def exists(self, f):
        return False


class Cons(List):
    def __init__(self, head, tail=None):
        self.h = head
        self.t = tail
        if tail:
            self.l = self.t.length() + 1  # noqa
        else:
            self.l = 1  # noqa

    def head(self):
        return self.h

    def tail(self):
        return self.t

    def isEmpty(self):
        return False

    def setHead(self, h):
        return Cons(h, self.t)

    def __str__(self):
        return "[{}NIL]".format(self.toString("", self).eval())

    def toString(self, sb, alist):
        return ret(sb) if alist.isEmpty() else sus(Supplier(self.toString, sb + "{}, ".format(alist.h), alist.t))

    def drop(self, n):
        return self._drop(self, n).eval()

    def _drop(self, alist, n):
        return ret(alist) if n <= 0 or alist.isEmpty() else sus(Supplier(self._drop, alist.t, n - 1))

    def dropWhile(self, f):
        return self._dropWhile(self, f).eval()

    def _dropWhile(self, alist, f):
        return sus(Supplier(self._dropWhile, alist.t, f)) if not alist.isEmpty() and f(alist.h) else ret(alist)

    def reverse(self):
        return self._reverse(nil, self).eval()

    def _reverse(self, acc, alist):
        return ret(acc) if alist.isEmpty() else sus(Supplier(self._reverse, Cons(alist.h, acc), alist.t))

    def init(self):
        return self.reverse().tail().reverse()

    def size(self):
        return 1 if self.t.isEmpty() else 1 + self.t.size()

    def length(self):
        return self.l

    def map(self, f):
        return self.foldRight(nil, lambda h, t: Cons(f(h), t))

    def flatMap(self, f):
        return self.foldRight(fl(), lambda e, a: concat(f(e), a))

    def filter(self, f):
        return self.foldRight(fl(), lambda e, a: Cons(e, a) if f(e) else a)

    def append(self, a):
        return None

    def foldRight(self, identity, f):
        return self._foldRight(identity, self.reverse(), identity, f).eval()

    def _foldRight(self, acc, alist, identity, f):
        return ret(acc) if alist.isEmpty() else sus(Supplier(self._foldRight, f(alist.h, acc), alist.t, identity, f))

    def headOption(self):
        raise UOException('headOption called on an empty list')

    def exists(self, f):
        r'''
        @Need to be enhanced by fold operation
        '''
        return f(self.head()) or self.tail().exists(f)


nil = Nil()


###################################
# Common Utility Function
###################################

def fl(*args):
    r'''
    Create List with element as given input

    @param flat(bool):
        True to flatten the element as list (First level only)
    '''
    if len(args) == 0:
        return nil
    else:
        sn = nil
        for i in range(len(args)):
            e = args[-1 * (i + 1)]
            if isinstance(e, list):
                for se in e:
                    sn = Cons(se, sn)
            elif isinstance(e, range):
                for se in e:
                    sn = Cons(se, sn)
            else:
                sn = Cons(args[-1 * (i + 1)], sn)
        return sn


def concat(list1, list2):
    r'''
    Concatenate input two list
    '''
    return list1 if list2.isEmpty() else _concat(list1.reverse(), list2).eval()


def _concat(list1, list2):
    return ret(list2) if list1.isEmpty() else sus(Supplier(_concat, list1.t, Cons(list1.h, list2)))


def fsum(alist):
    r'''
    * For an empty list: 0
    * For a non-empty list: head plus the sum of the tail
    '''
    return 0 if alist.isEmpty() else alist.foldRight(0, lambda e, a: e + a)


def fproduct(alist):
    r'''
    * For an empty list: 1.0
    * For a non-empty list: head * product of tail
    '''
    return 1.0 if alist.isEmpty() else alist.foldRight(1.0, lambda e, a: e * a)


def flatten(alist):
    r'''
    Method for flattening a list of lists into a list containing all elements of each contained list
    '''
    return alist.foldRight(fl(), lambda e, a: concat(e, a))
