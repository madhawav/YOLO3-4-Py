import os
import os.path as osp
from distutils.command.build import build
from distutils.command.clean import clean
from setup_util import setup_darknet, clean_darknet
import logging

try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command.build_ext import build_ext

    use_cython = False
else:
    use_cython = True

logging.basicConfig(level=logging.INFO)


def generate_command_class(params):
    """
    Generates the custom commands used by setup.
    :param: params: Parameters of setup.
    """

    class CustomBuild(build):
        """
        Build the package.
        """

        def run(self):
            # This is triggered when src distribution is made. Not triggered for build_ext.
            setup_darknet(download_darknet=params.darknet_download_required, target_location=osp.join(
                osp.dirname(osp.abspath(__file__)), "__libdarknet", "libdarknet.so"), darknet_url=params.darknet_url,
                          darknet_dir=params.darknet_home, build_branch_name=params.darknet_branch_name)
            build.run(self)

    class CustomBuildExt(build_ext):
        """
        Build extensions such as cython files.
        The compiled cython files (which become C files) are packaged with the source distribution.
        """

        def run(self):
            try:
                setup_darknet(download_darknet=params.darknet_download_required, darknet_url=params.darknet_url,
                              target_location=osp.join(osp.dirname(osp.abspath(__file__)), "__libdarknet",
                                                       "libdarknet.so"),
                              darknet_dir=params.darknet_home, build_branch_name=params.darknet_branch_name)
                build_ext.run(self)
            finally:
                if params.darknet_download_required:
                    clean_darknet(params.darknet_home)

    class CustomClean(clean):
        """
        Clean operation
        """

        def run(self):
            if osp.exists(osp.join(osp.dirname(osp.abspath(__file__)), "__libdarknet", "libdarknet.so")):
                logging.info("Removing __libdarknet/libdarknet.so")
                os.remove(osp.join(osp.dirname(__file__), "__libdarknet", "libdarknet.so"))

            if osp.exists(osp.join(osp.dirname(osp.abspath(__file__)), "libdarknet.so")):
                logging.info("Removing libdarknet.so")
                os.remove(osp.join(osp.dirname(osp.abspath(__file__)), "libdarknet.so"))

            if osp.exists(osp.join(osp.dirname(osp.abspath(__file__)), "pydarknet.cpp")):
                logging.info("Removing pydarknet.cpp")
                os.remove(osp.join(osp.dirname(osp.abspath(__file__)), "pydarknet.cpp"))

            for f in os.listdir(osp.dirname(osp.abspath(__file__))):
                if f.startswith("pydarknet.") and f.endswith(".so"):
                    logging.info("Removing " + f)
                    os.remove(osp.join(osp.dirname(osp.abspath(__file__)), f))

            clean.run(self)

    return {'clean': CustomClean, "build": CustomBuild, "build_ext": CustomBuildExt}
