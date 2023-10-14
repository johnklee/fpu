# Copyright 2017 The Abseil Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Adds support for parameterized tests to Python's unittest TestCase class."""
import logging
from functools import partial


class NoTestsError(Exception):
  """Raised when parameterized decorators do not generate any tests."""


def named_parameters(*test_cases):
  """A decorator for creating parameterized tests.

  Args:
    *testcases: Parameters for the decorated method, either a single iterable,
        or a list of tuples or dicts.

  Raises:
    NoTestsError: Raised when the decorator generates no tests.

  Returns:
     A decorated unit test case to include all the given test cases
  """
  def decorator(unit_test_case_func):
    if not test_cases:
      raise NoTestsError()

    def wrapper(*args, **kwargs):
      unit_test_case_object = args[0]
      unit_test_case_func_name = unit_test_case_func.__name__
      failed_test_case_list = []
      for test_case in test_cases:
        test_case_name = test_case['testcase_name'].replace(' ', '_')
        test_case['self'] = unit_test_case_object
        new_unit_test_case_name = (
            f'{unit_test_case_func_name}_{test_case_name}')
        logging.debug(f'Generating new test case={new_unit_test_case_name}')
        partial_unit_test_case_func = partial(
            unit_test_case_func, **test_case)
        try:
          partial_unit_test_case_func()
        except Exception as ex:
          failed_test_case_list.append(test_case['testcase_name'])

      if failed_test_case_list:
        raise AssertionError(
            f'Failed test case(s): {", ".join(failed_test_case_list)}')

    return wrapper

  return decorator
