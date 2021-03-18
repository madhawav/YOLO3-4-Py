import numpy as np
from setup_params import Params, PACKAGE_NAME_GPU, PACKAGE_NAME_CPU
from setuptools import setup, Extension
from setup_util import get_cflags, get_libs, find_site_packages, get_readme, \
    find_dist_packages, get_python_libs, get_python_cflags
import logging
import os
from setup_custom_commands import generate_command_class

# Compile using .cpp files if cython is not present
try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command.build_ext import build_ext

    use_cython = False
else:
    use_cython = True

logging.basicConfig(level=logging.INFO)

# Load setup parameters
params = Params.load_params()

# Configure source compilation args
include_paths = [np.get_include(), os.path.join(params.darknet_home, "include"),
                 os.path.join(params.darknet_home, "src")]
libraries = ["darknet", "m", "pthread"]
library_paths = [".", "./__libdarknet"]

extra_compiler_flags = get_python_cflags()
extra_linker_flags = get_python_libs()

cython_compile_directives = {}
macros = []

if params.use_gpu:
    include_paths.append(os.path.join(params.cuda_home, "include"))
    cython_compile_directives["USE_GPU"] = 1
    macros.append(("USE_GPU", 1))
else:
    cython_compile_directives["USE_GPU"] = 0
    macros.append(("USE_GPU", 0))

if params.use_cv:
    extra_compiler_flags.extend(get_cflags("opencv"))
    extra_linker_flags.extend(get_libs("opencv"))
    cython_compile_directives["USE_CV"] = 1
    macros.append(("USE_CV", 1))
else:
    cython_compile_directives["USE_CV"] = 0
    macros.append(("USE_CV", 0))

# Add linker flag to search in site_packages/__libdarknet. libdarknet.so is located at this location.
for site_package in find_site_packages():
    extra_linker_flags.append("-Wl,-rpath," + os.path.join(site_package, "__libdarknet"))

for dist_package in find_dist_packages():
    extra_linker_flags.append("-Wl,-rpath," + os.path.join(dist_package, "__libdarknet"))

# Configure extensions
if use_cython:
    pydarknet_extension = Extension("pydarknet", ["pydarknet.pyx", "pydarknet.pxd", "bridge.cpp"],
                                    include_dirs=include_paths, language="c++",
                                    libraries=libraries, library_dirs=library_paths, extra_link_args=extra_linker_flags,
                                    extra_compile_args=extra_compiler_flags, define_macros=macros)

    # Pass macros to Cython
    pydarknet_extension.cython_compile_time_env = cython_compile_directives
else:
    # NOTE: It is assumed that pydarknet.cpp is already generated using pydarknet.py. It is also assumed that params.use_cv
    # flag is unchanged between cythonize and current compilation.
    pydarknet_extension = Extension("pydarknet", ["pydarknet.cpp", "bridge.cpp"],
                                    include_dirs=include_paths, language="c++",
                                    libraries=libraries, library_dirs=library_paths, extra_link_args=extra_linker_flags,
                                    extra_compile_args=extra_compiler_flags, define_macros=macros)

ext_modules = [
    pydarknet_extension
]
cmd_class = generate_command_class(params)

# Identify package name based on gpu flag
if params.use_gpu:
    name = PACKAGE_NAME_GPU
else:
    name = PACKAGE_NAME_CPU

setup(
    name=name,
    description="Python wrapper on YOLO 3.0 implementation by 'pjreddie': (https://pjreddie.com/yolo)",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    cmdclass=cmd_class,
    version='0.2',
    ext_modules=ext_modules,
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
    zip_safe=False,
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
