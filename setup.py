import tempfile
from distutils.command.build import build
from distutils.command.clean import clean
import sys
import numpy as np # TODO: Need a mechanism to ensure numpy is already installed
import shutil

# Compile using .cpp files if cython is not present
try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command.build_ext import build_ext
    use_cython = False
else:
    use_cython = True

from setuptools import setup, Extension
from util import build_darknet, clean_darknet, get_cflags, get_libs, find_site_packages, get_readme, find_dist_packages
import logging
import os

logging.basicConfig(level=logging.INFO)

# Default configuration
USE_GPU = False
USE_CV = False

if "GPU" in os.environ:
    if "DARKNET_HOME" in os.environ:
        logging.warning("GPU environment variable is skipped since DARKNET_HOME is specified")
    else:
        if int(os.environ["GPU"]) == 1:
            logging.info("Darknet will be compiled with GPU support")
            USE_GPU = True
        else:
            logging.info("Darknet will be compiled without GPU support")
            USE_GPU = False


if "OPENCV" in os.environ and int(os.environ["OPENCV"]) == 0:
    logging.info("Compiling wrapper without OpenCV")
    USE_CV = False
elif "OPENCV" in os.environ and int(os.environ["OPENCV"]) == 1:
    logging.info("Compiling wrapper with OpenCV")
    USE_CV = True

if USE_CV & (get_libs("opencv") == '' or get_cflags("opencv") == ''):
    logging.warning("OpenCV is not configured. Compiling wrapper without OpenCV!")
    USE_CV = False


if USE_GPU:
    if USE_CV:
        build_branch_name = "yolo34py-intergration"
    else:
        build_branch_name = "yolo34py-intergration-nocv"
else:
    build_branch_name = "yolo34py-intergration-nogpu"
    if "DARKNET_HOME" not in os.environ:
        if USE_CV:
            logging.warning("Non GPU darknet branch is used. Compiling wrapper without OpenCV!")
        USE_CV = False # OpenCV requires yolo34py-intergration branch which has OpenCV enabled

if "DARKNET_HOME" not in os.environ:
    logging.info("Selected Darknet Branch: " + build_branch_name+ " from Darknet Fork 'https://github.com/madhawav/darknet/'")


temp_dir =  os.path.join(tempfile.gettempdir(), "darknet") # Temp directory to build darknet

# Check whether user has specified DARKNET_HOME directory. If so, we would use the darknet installation at this location.
if not "DARKNET_HOME" in os.environ:
    darknet_dir = os.path.join(temp_dir, "darknet-" + build_branch_name)
else:
    logging.info("DARKNET_HOME is set: " + os.environ["DARKNET_HOME"])
    darknet_dir = os.environ["DARKNET_HOME"]

include_paths = [np.get_include(), os.path.join(darknet_dir,"include"), os.path.join(darknet_dir,"src")]
libraries = ["darknet","m", "pthread"]
library_paths = [".", "./__libdarknet"]

extra_compiler_flags = [ get_cflags("python3")]
extra_linker_flags = [get_libs("python3")]

cython_compile_directives = {}
macros = []

if USE_CV:
    extra_compiler_flags.append(get_cflags("opencv"))
    extra_linker_flags.append(get_libs("opencv"))
    cython_compile_directives["USE_CV"] = 1
    macros.append(("USE_CV", 1))
else:
    cython_compile_directives["USE_CV"] = 0
    macros.append(("USE_CV", 0))


# Add linker flag to search in site_packages/__libdarknet. libdarknet.so is located at this location.
for site_package in find_site_packages():
    extra_linker_flags.append("-Wl,-rpath," + os.path.join(site_package,"__libdarknet"))

for dist_package in find_dist_packages():
    extra_linker_flags.append("-Wl,-rpath," + os.path.join(dist_package,"__libdarknet"))

if "--inplace" in sys.argv:
    extra_linker_flags.append("-Wl,-rpath,.")  # Added to make test code work

if use_cython:
    pydarknet_extension = Extension("pydarknet", ["pydarknet.pyx", "pydarknet.pxd", "bridge.cpp"], include_dirs=include_paths, language="c++",
                  libraries=libraries, library_dirs=library_paths,   extra_link_args=extra_linker_flags,
                  extra_compile_args=extra_compiler_flags, define_macros = macros)

    # Pass macros to Cython
    pydarknet_extension.cython_compile_time_env = cython_compile_directives
else:
    pydarknet_extension = Extension("pydarknet", ["pydarknet.cpp", "bridge.cpp"],
                                    include_dirs=include_paths, language="c++",
                                    libraries=libraries, library_dirs=library_paths, extra_link_args=extra_linker_flags,
                                    extra_compile_args=extra_compiler_flags, define_macros=macros)

    # NOTE: It is assumed that pydarknet.cpp is already generated using pydarknet.py. It is also assumed that USE_CV
    # flag is unchanged between cythonize and current compilation.

ext_modules=[
    pydarknet_extension
]

darknet_setup_done = False

def setup_darknet():
    '''
    Configures darknet on which the wrapper works
    :return:
    '''
    global darknet_setup_done
    if darknet_setup_done:
        return

    target_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "__libdarknet", "libdarknet.so")

    if "--inplace" in sys.argv:
        logging.info("For inplace compilations, target location is set to root")
        target_location =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "libdarknet.so")

    if "DARKNET_HOME" not in os.environ:
        # If user has not specified DARKNET_HOME, we will download and build darknet.
        build_darknet(temp_dir, build_branch_name, target_location)
    else:
        logging.info("Copying libdarknet.so from " + os.environ["DARKNET_HOME"])
        # If user has set DARKNET_HOME, it is assumed that he has built darknet. We will copy libdarknet.so from users location to site-pacakges/__libdarknet
        shutil.copyfile(os.path.join(os.environ["DARKNET_HOME"], "libdarknet.so"),
                        target_location)

    darknet_setup_done = True

class CustomBuild(build):
    def run(self):
        # This is triggered when src distribution is made. Not triggered for build_ext.
        setup_darknet()
        build.run(self)

class CustomBuildExt(build_ext):
    def run(self):
        setup_darknet()
        build_ext.run(self)

        if not "DARKNET_HOME" in os.environ:
            clean_darknet(temp_dir)

class CustomClean(clean):
    def run(self):
        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"__libdarknet","libdarknet.so")):
            logging.info("removing __libdarknet/libdarknet.so")
            os.remove(os.path.join(os.path.dirname(__file__),"__libdarknet","libdarknet.so"))

        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libdarknet.so")):
            logging.info("removing libdarknet.so")
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)),"libdarknet.so"))

        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"pydarknet.cpp")):
            logging.info("removing pydarknet.cpp")
            os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)),"pydarknet.cpp"))

        for f in os.listdir(os.path.dirname(os.path.abspath(__file__))):
            if f.startswith("pydarknet.") and f.endswith(".so"):
                logging.info("removing " + f)
                os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)),f))

        clean.run(self)


if USE_GPU:
    name = "yolo34py-gpu"
else:
    name = "yolo34py"

cmd_class = {'clean': CustomClean, "build": CustomBuild, "build_ext": CustomBuildExt}


setup(
  name = name,
  description="Python wrapper on YOLO 3.0 implementation by 'pjreddie': (https://pjreddie.com/yolo)",
  long_description=get_readme(),
  long_description_content_type="text/markdown",
  cmdclass= cmd_class,
  version='0.1.rc12',
  ext_modules = ext_modules,
  platforms=["linux-x86_64"],
  setup_requires=[
      'cython>=0.27',
      'requests',
      'numpy'
  ],
  install_requires=[
      'cython>=0.27',
      'requests',
      'numpy'
  ],
  python_requires='>=3.5',
  author='Madhawa Vidanapathirana',
  author_email='madhawavidanapathirana@gmail.com',
  url="https://github.com/madhawav/YOLO3-4-Py",
  package_dir={"__libdarknet": "__libdarknet"},
  packages=["__libdarknet"],
  include_package_data=True,
  license="YOLO34Py wrapper is under Apache 2.0. Darknet is Public Domain.",
  classifiers=[
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Topic :: Text Processing :: Linguistic',
      'Operating System :: POSIX :: Linux',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering :: Artificial Intelligence'
  ],
  keywords="yolo darknet object detection vision",

)
