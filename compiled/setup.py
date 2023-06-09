from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension

ext_modules = [
    Extension(
        "cython_module",  # Your module name
        sources=["cython_module.pyx"],
        language="c++",  # This is the crucial part
    )
]

setup(
    name="CythonModule",
    ext_modules=cythonize(ext_modules),
)
