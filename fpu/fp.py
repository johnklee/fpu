"""This module is created to let Python support FP (Function Programming)."""
import functools
import logging
from abc import ABCMeta, abstractmethod
try:
  from utils import *     # noqa
except:                     # noqa
  from .utils import *    # noqa


################################
# API Segment
################################


def compose2(f, g):
  def m(*args):
    return f(g(*args))

  return m


def compose(*functions):
  def m(*args):
    return args

  return functools.reduce(compose2, functions, m)


def andThen(f, g):
  def m(*args):
    return g(f(*args))

  return m


################################
# Class Segment
################################
@aliased
class Option:
  __metaclass__ = ABCMeta

  @abstractmethod
  def map(self, func):
    raise NotImplementedError()

  @abstractmethod
  def getOrElse(self, supr):
    """Method that will return either the contained value if it exists,
    or return the result by executing the given `supr` object.
    """
    raise NotImplementedError()

  @abstractmethod
  def getOr(self, dft):
    """This method that will return either the contained value if it exists,
    or a provided default one otherwise.
    """
    raise NotImplementedError()

  @abstractmethod
  def isSome(self):
    raise NotImplementedError()

  @abstractmethod
  def getOrThrow(self):
    raise NotImplementedError()

  @staticmethod
  def some(value):
    return Some(value)

  @staticmethod
  def none():
    return N()

  @alias('fm')
  def flatMap(self, func):
    return self.map(func).getOrElse(Option.none)

  def orElse(self, supr):
    return self.map(lambda e: self).getOrElse(supr)

  def filter(self, func):
    return self.flatMap(lambda e: self if func(e) else Option.none())


class N(Option):
  def map(self, func):
    return self

  def getOr(self, dft):
    return dft

  def getOrElse(self, supr):
    return supr()

  def isSome(self):
    return False

  def getOrThrow(self):
    raise Exception('get called on None')

  def __eq__(self, other):
    return isinstance(other, N)

  def __str__(self):
    return "None()"

  def __hash__(self):
    return hash(0)


class Some(Option):
  def __init__(self, value):
    self.value = value

  def map(self, func):
    return Some(func(self.value))

  def getOr(self, dft):
    return self.value

  def getOrElse(self, supr):
    return self.value

  def isSome(self):
    return True

  def getOrThrow(self):
    return self.value

  def __eq__(self, other):
    return (
      True
      if isinstance(other, Some) and (
        self.value == other.value or self.value == other)
      else False
    )

  def __str__(self):
    return "Some({})".format(self.value)

  def __hash__(self):
    return hash(self.value)


class Supplier:
  def __init__(self, func, *args):
    self.func = func
    self.args = args

  def __call__(self):
    return self.func(*self.args)


class Case:
  def __init__(self, cond, rst):
    """

    Attributes:
      cond(Callable): Condition object
      rst(Callable): Clause to execute after matching
    """
    self.cond = cond    # Callable
    self.rst = rst      # Callable

  @staticmethod
  def mcase(cond, rst):
    """Conditional clause."""
    return Case(cond, rst)

  @staticmethod
  def default(rst):
    """Default clause."""
    return Case(None, rst)

  @staticmethod
  def match(dftCase, *matches):
    """Perform matching clause."""
    for m in matches:
      if m.cond is None:
        return m.rst() if callable(m.rst) else m.rst
      elif m.cond():
        return m.rst() if callable(m.rst) else m.rst

    return dftCase.rst() if callable(dftCase.rst) else dftCase.rst


class Effect:
  """Abstract class to be implemented as functional object."""

  __metaclass__ = ABCMeta

  def __call__(self, value):
    self.call(value)

  @abstractmethod
  def call(self, value):
    raise NotImplementedError()


class Result:
  __metaclass__ = ABCMeta

  @staticmethod
  def failure(message):
    return Failure(message)

  @staticmethod
  def success(value=None):
    return Success(value)

  @staticmethod
  def empty():
    return Empty()

  @abstractmethod
  def bind(self, successEff, failureEff):
    raise NotImplementedError()

  @abstractmethod
  def getOrElse(defaultVal):
    raise NotImplementedError()

  @abstractmethod
  def map(func):
    raise NotImplementedError()


class Empty(Result):
  def __init__(self):
    pass

  def bind(self, successEff, failureEff):
    return failureEff('Empty')

  def __str__(self):
    return "Empty()"

  def getOrElse(self, defaultVal):
    if isinstance(defaultVal, Supplier):
      return defaultVal()

    return defaultVal

  def map(self, func):
    return self


class Success(Result):
  def __init__(self, value):
    self.value = value

  def bind(self, successEff, failureEff):
    return successEff(self.value)

  def getOrElse(self, defaultVal):
    return self.value

  def map(self, func):
    try:
      return Success(func(self.value))
    except:
      logging.exception('Fail to apply {}'.format(func))
      return Failure('Error while applying {}'.format(func))

  def __str__(self):
    return "Success({})".format(self.value)


class Failure(Result):
  def __init__(self, message):
    self.message = message

  def bind(self, successEff, failureEff):
    return failureEff(self.message)

  def __str__(self):
    return "Failure({})".format(self.message)

  def getOrElse(self, defaultVal):
    if isinstance(defaultVal, Supplier):
      return defaultVal()
    return defaultVal

  def map(self, func):
    return self


class TailCall:
  __metaclass__ = ABCMeta

  @abstractmethod
  def resume(self):
    raise NotImplementedError()

  @abstractmethod
  def eval(self):
    raise NotImplementedError()

  @abstractmethod
  def isSuspend(self):
    raise NotImplementedError()

  @staticmethod
  def ret(t):
    return Return(t)

  @staticmethod
  def sus(resume):
    return Suspend(resume)


class Suspend(TailCall):
  def __init__(self, resume):
    self.resume = resume

  def isSuspend(self):
    return True

  def resume(self):
    return self.resume()

  def eval(self):
    tc = self
    while tc.isSuspend():
      tc = tc.resume()

    return tc.eval()


class Return(TailCall):
  def __init__(self, t):
    self.t = t

  def isSuspend(self):
    return False

  def resume(self):
    raise NotImplementedError()

  def eval(self):
    return self.t


class Fun:
  def __init__(self, f):
    self.f = f

  def compose(self, of):
    return Fun(compose(self, of))

  def andThen(self, of):
    return Fun(compose(of, self))

  def __call__(self, *args):
    return self.f(*args)


class CollectionUtils:
  """Collection utilities used in FP."""

  @staticmethod
  def l(*args):  # noqa
    alist = []
    alist.extend(args)
    return alist

  @staticmethod
  def fl(tlist):
    alist = []
    alist.extend(tlist)
    return tuple(alist)

  @staticmethod
  def m(alist, fun):
    nlist = CollectionUtils.l()
    for e in alist:
      nlist.append(fun(e))

    return tuple(nlist)

  @staticmethod
  def head(alist):
    if len(alist) == 0:
      raise Exception('Input list with length as 0')
    return CollectionUtils.l(alist[0])

  @staticmethod
  def copy(alist):
    nlist = CollectionUtils.l()
    nlist.extend(alist)
    return tuple(nlist)

  @staticmethod
  def tail(alist):
    if len(alist) == 0:
        raise Exception('Input list with length as 0')
    nlist = list(CollectionUtils.copy(alist))
    del nlist[0]
    return tuple(nlist)

  @staticmethod
  def append(alist, e):
    nlist = list(CollectionUtils.copy(alist))
    nlist.append(e)
    return tuple(nlist)

  @staticmethod
  def first(alist, fun):
    for e in alist:
      if fun(e):
        return CollectionUtils.l(e)
    return CollectionUtils.l()

  @staticmethod
  def foldLeft(alist, identity, fun):
    rst = identity
    for e in alist:
      rst = fun(rst, e)
    return rst

  @staticmethod
  def foldRight(alist, identity, fun):
    rst = identity
    for e in reversed(alist):
      rst = fun(e, rst)

    return rst

  @staticmethod
  def reverse(alist):
    nlist = CollectionUtils.l()
    for e in reversed(alist):
      nlist.append(e)

    return tuple(nlist)

  @staticmethod
  def prepend(alist, e):
    nlist = list(CollectionUtils.copy(alist))
    nlist.insert(0, e)
    return nlist

  @staticmethod
  def forEach(alist, fun):
    for e in alist:
      fun(e)

  @staticmethod
  def unfold(seed, f, p):
    """Unfold operation.

     Args:
        seed: The input argument of second and third callable object
        f(callable): Generate the next value for collection
        p(callable): Callable to terminate the process by returning True
    """
    nlist = CollectionUtils.l()
    temp = seed
    while p(temp):
        nlist.append(temp)
        temp = f(temp)

    return tuple(nlist)

  @staticmethod
  def range(start, end, step=1, e_inclusive=False):
    if e_inclusive:
      return CollectionUtils.unfold(
        start, lambda e: e + step, lambda e: e <= end
      )

    return CollectionUtils.unfold(
      start, lambda e: e + step, lambda e: e < end
    )
