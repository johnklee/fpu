from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import fpu

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

long_description = read('README.md')

setup(name='fpu',
      version=fpu.__version__,
      description='Functional Programming Utility',
      url='https://github.com/johnklee/fpu',
      author='johnklee',
      author_email='puremonkey2007@gmail.com',
      tests_require=['pytest'],
      long_description_content_type='text/markdown',
      long_description=long_description,
      license='MIT',
      packages=['fpu'],
      classifiers = [
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      zip_safe=False)
