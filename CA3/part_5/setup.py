from distutils.core import setup
from Cython.Build import cythonize


setup(ext_modules =cythonize(["c1.pyx", "c2.pyx", "c3.pyx", "c4.pyx"]))