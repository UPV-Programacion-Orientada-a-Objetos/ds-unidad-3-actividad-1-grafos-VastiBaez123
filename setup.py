from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Define the extension module
extensions = [
    Extension(
        "neuronet",
        sources=["cython/neuronet.pyx", "cpp/GrafoDisperso.cpp"],
        include_dirs=["cpp"],
        language="c++",
        extra_compile_args=["-std=c++11"],
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
)
