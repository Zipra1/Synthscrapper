# This script is for generating C code from Python, to improve speed of calculations.

from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize('enemies_cy.pyx'))