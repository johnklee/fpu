#!/usr/bin/env python
from fpu.fp import *
from fpu.flist import *

sus = TailCall.sus
ret = TailCall.ret

def unfold(z, func):
    out = _unfold(fl(), z, func)
    #print("out={}".format(out.eval()))
    return out.eval().reverse()


def _unfold(acc, z, func):
    r = func(z)  # Result object
    #print("_unfold: {}".format(r))
    rt = r.map(lambda e: sus(Supplier(_unfold, acc.cons(e[0]), e[1], func)))
    #print("rt: {}".format(rt))
    frt = rt.getOrElse(ret(acc))
    #print("frt: {}".format(frt))
    return frt

alist = unfold(0, lambda i: Result.success([i, i + 1]) if i < 10 else Result.empty())
print(alist)
