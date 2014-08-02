from distutils.core import setup, Extension
import numpy.distutils.misc_util

__version__ = "0.1"

cdiffusion = Extension(
    'cdiffusion',
    sources=['../diffusion.c', 'cdiffusion/python_interface.c'],
    extra_compile_args=["-O3", "-std=c99", "-Wall", "-p", "-pg", ],
    extra_link_args=["-lc"],
)

setup(
    name='diffusion',
    version=__version__,
    ext_modules=[cdiffusion, ],
    packages=["diffusion", ],
    include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
)
