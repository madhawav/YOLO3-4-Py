from distutils.command.clean import clean
from distutils.core import setup
from Cython.Distutils.extension import Extension
import pkgconfig
import numpy as np
from Cython.Distutils import build_ext
import logging
import os

logging.basicConfig(level=logging.INFO)

USE_CV = True

if "NO_OPENCV" in os.environ and int(os.environ["NO_OPENCV"]) == 1:
    logging.info("Compiling without OpenCV")
    USE_CV = False

if USE_CV & (pkgconfig.libs("opencv") == '' or pkgconfig.cflags("opencv") == ''):
    logging.warning("OpenCV is not configured. Compiling without OpenCV!")
    USE_CV = False

if not "DARKNET_HOME" in os.environ:
    darknet_dir = input("$DARKNET_HOME:")
else:
    darknet_dir = os.environ["DARKNET_HOME"]

include_paths = [np.get_include(), os.path.join(darknet_dir,"include"), os.path.join(darknet_dir,"src")]
libraries = ["darknet", "m", "pthread"]
library_paths = [darknet_dir]

extra_compiler_flags = [ pkgconfig.cflags("python3")]
extra_linker_flags = [pkgconfig.libs("python3")]

cython_compile_directives = {}

if USE_CV:
    extra_linker_flags.append(pkgconfig.cflags("opencv"))
    extra_linker_flags.append(pkgconfig.libs("opencv"))
    cython_compile_directives["USE_CV"] = 1
else:
    cython_compile_directives["USE_CV"] = 0

ext_modules=[
    Extension("pydarknet", ["pydarknet.pyx", "pydarknet.pxd", "bridge.cpp"], include_dirs=include_paths, language="c++",
              libraries=libraries, library_dirs=library_paths,   extra_link_args=extra_linker_flags,
              cython_compile_time_env=cython_compile_directives,
              extra_compile_args=extra_compiler_flags),
]

class CustomClean(clean):
    def run(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__),"pydarknet.cpp")):
            print("removing pydarknet.cpp")
            os.remove(os.path.join(os.path.dirname(__file__),"pydarknet.cpp"))

        for f in os.listdir(os.path.dirname(os.path.abspath(__file__))):
            if f.startswith("pydarknet.") and f.endswith(".so"):
                print("removing", f)
                os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)),f))

        clean.run(self)

setup(
  name = 'PyDarknet',
  cmdclass={'build_ext': build_ext, 'clean': CustomClean},
  ext_modules = ext_modules,
  install_requires=[
      'cython>=0.27',
      'pkgconfig'
  ]
)