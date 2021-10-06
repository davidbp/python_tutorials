
"""
In order to build the cythoned version of a function the following command can be used:

python3 setup_cython_functions.py build_ext --inplace

This command should create a file:  juliacy.something.so

"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
import numpy as np

ext_modules = [Extension('juliacy',
              ["./cython_code/cy_func.pyx"],
	          extra_compile_args=['-fopenmp'],
	          extra_link_args=['-fopenmp'])]

from Cython.Build import cythonize
setup(ext_modules = cythonize(ext_modules,
	  compiler_directives={'language_level':'3'},),
      include_dirs=[np.get_include(), "/usr/local/opt/llvm/lib"])
     

