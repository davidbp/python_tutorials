"""
python3 compile.py build_ext --inplace
"""
from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(ext_modules=cythonize("./Edit_Distance_c.pyx"))
