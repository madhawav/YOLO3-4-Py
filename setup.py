from distutils.core import setup
from distutils.extension import Extension
import pkgconfig
import numpy as np

import os

from Cython.Distutils import build_ext

if not "DARKNET_HOME" in os.environ:
    darknet_dir = input("$DARKNET_HOME:")
else:
    darknet_dir = os.environ["DARKNET_HOME"]

include_paths = [np.get_include(), os.path.join(darknet_dir,"include"), os.path.join(darknet_dir,"src")]
libraries = ["darknet", "m", "pthread"]
library_paths = [darknet_dir]

extra_compiler_flags = [pkgconfig.cflags("opencv"), pkgconfig.cflags("python3")]
extra_linker_flags = [pkgconfig.libs("opencv"),pkgconfig.libs("python3")]

ext_modules=[
    Extension("pydarknet", ["pydarknet.pyx", "pydarknet.pxd", "bridge.cpp"], include_dirs=include_paths, language="c++",
              libraries=libraries, library_dirs=library_paths,   extra_link_args=extra_linker_flags,
              extra_compile_args=extra_compiler_flags),
]


setup(
  name = 'PyDarknet',
  cmdclass={'build_ext': build_ext},
  ext_modules = ext_modules
)