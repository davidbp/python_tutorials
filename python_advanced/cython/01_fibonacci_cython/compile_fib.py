"""
python3 compile_fib.py build_ext --inplace
"""
from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("./cython_code/fib_cy.pyx"))
