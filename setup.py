import tempfile

from distutils.command.clean import clean
from distutils.core import setup
from Cython.Distutils.extension import Extension
import pkgconfig
import numpy as np
import sys
import shutil

import os

from Cython.Distutils import build_ext
from setuptools import setup, Extension
from setuptools.command.build_py import build_py

from darknet_loader import build_darknet, clean_darknet
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


def find_site_packages():
    site_packages = [p for p in sys.path if p.endswith("site-packages") or p.endswith("site-packages/")]
    return site_packages


temp_dir =  os.path.join(tempfile.gettempdir(), "darknet")

# Check whether user has specified DARKNET_HOME directory. If so, we would use the darknet installation at this location.
if not "DARKNET_HOME" in os.environ:
    darknet_dir = os.path.join(temp_dir, "darknet-yolo34py-intergration")
else:
    print("DARKNET_HOME is set:", os.environ["DARKNET_HOME"])
    darknet_dir = os.environ["DARKNET_HOME"]


include_paths = [np.get_include(), os.path.join(darknet_dir,"include"), os.path.join(darknet_dir,"src")]
libraries = ["darknet","m", "pthread"]
library_paths = ["./__libdarknet"]

extra_compiler_flags = [ pkgconfig.cflags("python3")]
extra_linker_flags = [pkgconfig.libs("python3")]

cython_compile_directives = {}

if USE_CV:
    extra_linker_flags.append(pkgconfig.cflags("opencv"))
    extra_linker_flags.append(pkgconfig.libs("opencv"))
    cython_compile_directives["USE_CV"] = 1
else:
    cython_compile_directives["USE_CV"] = 0

# Add linker flag to search in site_packages/__libdarknet. libdarknet.so is located at this location.
for site_package in find_site_packages():
    extra_linker_flags.append("-Wl,-rpath," + os.path.join(site_package,"__libdarknet"))

ext_modules=[
    Extension("pydarknet", ["pydarknet.pyx", "pydarknet.pxd", "bridge.cpp"], include_dirs=include_paths, language="c++",
              libraries=libraries, library_dirs=library_paths,   extra_link_args=extra_linker_flags,
              cython_compile_time_env=cython_compile_directives,
              extra_compile_args=extra_compiler_flags),
]

class CustomBuildPy(build_py):
    def run(self):
        if "DARKNET_HOME" not in os.environ:
            # If user has not specified DARKNET_HOME, we will download and build darknet.
            build_darknet(temp_dir)
        else:
            # If user has set DARKNET_HOME, it is assumed that he has built darknet. We will copy libdarknet.so from users location to site-pacakges/__libdarknet
            shutil.copyfile(os.path.join(os.environ["DARKNET_HOME"],"libdarknet.so"),os.path.join(os.path.dirname(__file__),"__libdarknet","libdarknet.so"))
        build_py.run(self)

class CustomBuildExt(build_ext):
    def run(self):
        build_ext.run(self)
        # If user has set DARKNET_HOME, it is assumed that he has built darknet
        if not "DARKNET_HOME" in os.environ:
            clean_darknet(temp_dir)
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
  name = 'yolo34py',
  description="Python wrapper on YOLO 3.0 implementation by original authors 'pjreddie/darknet' (https://pjreddie.com/yolo)",
  long_description="This is a Python wrapper on YOLO 3.0 implementation provided by original authors of YOLO 3.0.",
  cmdclass={'build_ext': CustomBuildExt, 'clean': CustomClean, "build_py": CustomBuildPy},
  version='0.1.2rc',
  ext_modules = ext_modules,
  platforms=["linux-x86_64"],
  install_requires=[
      'cython>=0.27',
      'pkgconfig',
      'request'
  ],
  author='Madhawa Vidanapathirana',
  author_email='madhawavidanapathirana@gmail.com',
  url="https://github.com/madhawav/YOLO3-4-Py",
  package_dir={"__libdarknet": "__libdarknet"},
  packages=["__libdarknet"],
  include_package_data=True,
  license="YOLO34Py wrapper is under Apache 2.0. Darknet is Public Domain."
)