from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pathlib import Path
import fpu


def read(*parts):
  return Path(__file__).parent.joinpath(*parts).read_text()


long_description = read('README.md')
setup(
  name='fpu',
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
  classifiers=[
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  zip_safe=False
)
