#!/bin/env python
"""Solution for leetcode #2640 without FPU."""
from functools import reduce, partial
import numpy as np
from typing import List


class Solution:
    def findPrefixScore(self, nums: List[int]) -> List[int]:
        max_ary = [nums[0]]
        def append_list(a, b, ary):
            c = max(a, b)
            ary.append(c)
            return c

        max_append = partial(append_list, ary=max_ary)
        reduce(max_append, nums)

        conversion_ary = list(map(
            lambda t: t[1] + nums[t[0]],
            enumerate(max_ary)))

        return np.cumsum(conversion_ary).tolist()


if __name__ == '__main__':
  sol = Solution()
  for input_nums, expected_nums in (
      ([2,3,7,5,10], [4,10,24,36,56]),
      ([1,1,2,4,8,16], [2,4,8,16,32,64]),
  ):
    out = sol.findPrefixScore(input_nums)
    assert out == expected_nums

  print("Pass!")
