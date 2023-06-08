from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Cython Module',
    ext_modules=cythonize("cython_module.pyx"),
    zip_safe=False,
)
