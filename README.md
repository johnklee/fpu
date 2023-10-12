[![CI-Build](https://github.com/johnklee/fpu/actions/workflows/ci-build.yml/badge.svg?branch=master)](https://github.com/johnklee/fpu/actions/workflows/ci-build.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fpu)
[![Coverage Status](https://coveralls.io/repos/github/wkCircle/fpu/badge.svg?branch=19-badges)](https://coveralls.io/github/wkCircle/fpu?branch=19-badges)

Overview and Table of Contents
==========================
This package is used as utility to support more thorough FP (functional programming) functionalities in Python. For more, you can refer to [FPU.pptx](https://github.com/johnklee/fpu/blob/master/docs/FPU.pptx)

* [**FP Introduction**: Functional programming has a long history. In a nutshell, its a style of programming where you focus on transforming data through the use of small expressions that ideally don’t contain side effects.](#fpi)
    * [Feature of FP](#fpi_s1)
    * [Pro & Con of FP](#fpi_s2)
    * [Python's Functional Features](#fpi_s3)
* [**Example API Usage**: To have a taste on how this utility to help you to program in FP](#examples)
    * [Gemstones](#exp_gemstones)
* [**More about FP**: Appendix of other resources](#supplement)

# FP Introduction <a name='fpi'></a>
([Source link](https://www.youtube.com/watch?v=Ta1bAMOMFOI)) Functional programming has a long history. In a nutshell, its a style of programming where you focus on transforming data through the use of small expressions that ideally don’t contain side effects. In other words, when you call my_fun(1, 2), it will alway return the same result. This is achieved by immutable data typical of a functional language.
* Lisp 1958
* Renaissance: F#, Haskell, Erlang ...
* Used in industry such as Trading, Algorithmic, and Telecommunication etc

## Features of FP <a name='fpi_s1'></a>
* First-class function/Higher order function
* Pure functions without side effects
* Immutable data structures
* Preserve state in functions (Closure, Cury)
* Recursion instead of loops/iteration

### First-class function/Higher order function
With this feature, you can:
* Use function as argument(s)
* Function can return function
* Enables functional composition

Let's take a example to explain the usage of functional composition. Below is the imperative way to get the minimum value of all maximum values from values:
```python
dataSet = [{'values':[1, 2, 3]}, {'values':[4, 5]}]

# Imperative
def min_max_imp(dataSet):
    max_list = []
    for d in dataSet:
        max_list.append(max(d['values']))
        
    return min(max_list)

min_max_imp(dataSet) # 3
```
Above function `min_max_imp` actually comprises two sub steps:
* Get the maximum of each values
* Get the minimum of list collected by previous step

This implies you can compose above two steps (function) into one by leveraging exist functions:
```python
# FP
from fpu.fp import *
from functools import reduce, partial

# compose2(f, g) = f(g())
min_max = compose2(
                    partial(reduce, min), \
                    partial(map, lambda d: max(d['values']))
                  )
min_max(dataSet)
```
With composing feature, you can write less dump code and make use of exist function to generate new function!

### Pure functions without side effects
The [side effects](https://en.wikipedia.org/wiki/Side_effect_(computer_science)) can refer to many things.  I suggest you to read below materials to know more:
* [Get started with Functional Programming | otsconf 2015](https://www.youtube.com/watch?v=6f5dt923FmQ&t=96s)
* [Functional Programming with Python](https://www.youtube.com/watch?v=Ta1bAMOMFOI)

### Immutable data structures
There are many python packages support you to carry out this requirement. One of them is [**pyrsistent**](https://github.com/tobgu/pyrsistent). Below is a few usage of it to show `immutable data`:
```python
In [2]: v1 = v(1, 2, 3)                                                         

In [3]: v2 = v1.append(4) # Any operation on v1 will return new vectory to reflect the modification

In [4]: v1                                                                      
Out[4]: pvector([1, 2, 3])  # v1 stay immutable

In [5]: v2                                 
Out[5]: pvector([1, 2, 3, 4])  # v2 reflect the change for appending 4

In [6]: v3 = v2.set(1, 5)          

In [7]: v2                                                                      
Out[7]: pvector([1, 2, 3, 4])

In [8]: v3
Out[8]: pvector([1, 5, 3, 4])
```
Above is a demonstration on data structure vector. There are more for [**PMap**](https://github.com/tobgu/pyrsistent#pmap), [**PSet**](https://github.com/tobgu/pyrsistent#pset), [**PRecord**](https://github.com/tobgu/pyrsistent#precord) and [**PClass**](https://github.com/tobgu/pyrsistent#pclass).

### Preserve state in functions (Closure, Cury)
A [Closure](https://en.wikipedia.org/wiki/Closure_(computer_programming)) which simply creates a scope that allows the function to access and manipulate the variables in enclosing scopes. Normally, you will follow below steps to create a Closure in Python:
* We have to create a nested function (a function inside another function).
* This nested function has to refer to a variable defined inside the enclosing function.
* The enclosing function has to return the nested function

Below is a simple example to create closure:
```python
In [10]: def addN(n): 
    ...:     def _add(v): 
    ...:         return v + n 
    ...:     return _add 
    ...:                                                                                                                                                                                                           

In [11]: addOne = addN(1)                                                                                                                                                                                          

In [12]: addOne(2)                                                                                                                                                                                                 
Out[12]: 3

In [13]: addOne(3)                                                                                                                                                                                                 
Out[13]: 4

In [14]: addTwo = addN(2)                                                                                                                                                                                          

In [15]: addTwo(2)                                                                                                                                                                                                 
Out[15]: 4

In [16]: addTwo(3)                                                                                                                                                                                                 
Out[16]: 5
```
[Currying](https://en.wikipedia.org/wiki/Currying) is like a kind of incremental binding of function arguments. It is the technique of breaking down the evaluation of a function that takes multiple arguments into evaluating a sequence of single-argument functions:
* Concept by Haskell Curry
* Translating a function that takes multiple arguments into a sequence of functions which all take 1 argument. e.g.: `add(a, b)` AND `add(a)(b)`
* Improves reusability and composition
* In some languages (Haskell, F#) functions are curried by default

Unfortunately, Python doesn't support curring in default. Below is a workaround for you to do curring in Python3:
```python
from inspect import signature

def curry(x, argc=None):
    if argc is None:
        argc = len(signature(x).parameters)
        
    def p(*a):
        if len(a) == argc:
            return x(*a)
        def q(*b):
            return x(*(a + b))
        return curry(q, argc - len(a))
    return p

@curry
def myfun(a,b,c):
    print("{}-{}-{}".format(a,b,c))
    
myfun(1, 2, 3)
myfun(1, 2)(3)
myfun(1)(2)(3) 
```

### Recursion instead of loops/iteration
FP favors recursion over for-loop. However, the recursion will use precious resource as stack. You can use below sample code to retrieve the recursive limit:
```python
In [17]: import sys                                                                                                                                                                                                

In [18]: sys.getrecursionlimit()                                                                                                                                                                                   
Out[18]: 3000
```
This package use class **TailCall** to store the function call in heap instead of stack. Below is one usage example:
```python
In [1]: def fibRec(n, x=0, y=1): 
   ...:     if n == 0: 
   ...:         return x 
   ...:     else: 
   ...:         return fibRec(n-1, y, x + y) 
   ...:                                                                         

In [2]: fibRec(3)                                                               
Out[2]: 2

In [3]: fibRec(3000)                                                            
---------------------------------------------------------------------------
RecursionError                            Traceback (most recent call last)
<ipython-input-3-035cf1755b78> in <module>
----> 1 fibRec(3000)

<ipython-input-1-f509e891ef84> in fibRec(n, x, y)
      3         return x
      4     else:
----> 5         return fibRec(n-1, y, x + y)
      6 

... last 1 frames repeated, from the frame below ...

<ipython-input-1-f509e891ef84> in fibRec(n, x, y)
      3         return x
      4     else:
----> 5         return fibRec(n-1, y, x + y)
      6 

RecursionError: maximum recursion depth exceeded in comparison
```
The exception is raised owing to recursion limitation. We can get by this limition by adopting **TailCall**:
```python
In [5]: from fpu.fp import *                                                                                        

In [6]: ret = TailCall.ret; sus = TailCall.sus
In [22]: def fib(n, x=0, y=1):     
    ...:     return ret(x) if n == 0 else sus(Supplier(fib, n-1, y, x + y)) 
    ...:                                                                                                                                                                                                           

In [23]: fib(3)                                                                                                                                                                                                    
Out[23]: <fpu.fp.Suspend at 0x7f2be96be710>

In [24]: fib(3).eval()                                                                                                                                                                                             
Out[24]: 2

In [25]: fib(3000).eval()                                                                                                                                                                                          
Out[25]: 410615886307971260333568378719267105220125108637369252408885430926905584274113403731330491660850044560830036835706942274588569362145476502674373045446852160486606292497360503469773453733196887405847255290082049086907512622059054542195889758031109222670849274793859539133318371244795543147611073276240066737934085191731810993201706776838934766764778739502174470268627820918553842225858306408301661862900358266857238210235802504351951472997919676524004784236376453347268364152648346245840573214241419937917242918602639810097866942392015404620153818671425739835074851396421139982713640679581178458198658692285968043243656709796000
```

## Pro & Con of FP <a name='fpi_s2'></a>
Here we will be going to review what advantage/disadvantage FP will bring to you.

### Advantages of FP
* Absence of side effects can make your programs more robust
* Programs tend to be more modular come and typically in smaller building blocks
* Better testable - call with same parameters always returns same result
* Focus on algorithms
* Conceptional fit with parallel / concurrent programming
* Live upates - Install new release while running

### Disadvantages of FP
* Solutions to the same problem can look very different than procedural/OO ones
* Finding good developers can be hard
* Not equally useful for all types of problems
* Input/Output are side effects and need special treatment
* Recursion is "an order of magnitude more complex" than loops/iterations
* Immutable data structures may increase run times

## Python's Functional Features - Overview <a name='fpi_s3'></a>
* Pure functions (sort of)
* Closures - hold state in functions
* Functions as objects and decorators
* Immutable data types (tuple, freezeSet)
* Lazy evaluation - generators
* List (dictionary, set) comprehensions
* [functools](https://docs.python.org/3.5/library/functools.html), itertools, lambda, map, filter
* Recursion - try to avoid, recursion limit has a reason

# Example API Usage <a name='examples'></a>
Here we are going to look at few examples from [HackerRank](https://www.hackerrank.com/) to know how FP can help you write code gracefully.

## Gemstones <a name='exp_gemstones'>
The [problem](https://www.hackerrank.com/challenges/gem-stones/problem) simply ask you to extract element exist in every rock. The imperative approach will look like:
```python
arr = ['abcdde', 'baccd', 'eeabg']
# Complete the gemstones function below.
def gemstones_imp(arr):
    set_list = []
    for s in arr:
        set_list.append(set(list(s)))

    # Imperative code
    uset = None
    for aset in set_list:
        if uset is None:
            uset = aset
        else:
            uset = uset & aset

    return len(uset)

print("Output of gemstones_imp={}".format(gemstones_imp(arr)))
``` 
The FP (declarative approach) code will be neat and graceful:
```python
from fpu.flist import *

def gemstones_dec(arr):
    rlist = fl(arr)
    return len(
                rlist.map(lambda r: set(list(r))) \
                     .reduce(lambda a, b: a & b)
              )

print("Output of gemstones_imp={}".format(gemstones_dec(arr)))
```

# Supplement <a name='supplement'></a>
* [FP In Python - Ch1. (Avoiding) Flow Control](http://puremonkey2010.blogspot.com/2018/05/fp-in-python-ch1-avoiding-flow-control.html)
* [FP In Python - Ch2. Callables](http://puremonkey2010.blogspot.com/2018/05/fp-in-python-ch2-callables.html)
* [FP In Python - Ch3. Lazy Evaluation](http://puremonkey2010.blogspot.com/2018/05/fp-in-python-ch3-lazy-evaluation.html)
