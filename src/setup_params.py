import os.path as osp
import tempfile
from setup_util import get_libs, get_cflags
import logging
import os

logging.basicConfig(level=logging.INFO)

DARKNET_GPU_OPENCV_BRANCH = "yolo34py-intergration-v2"
DARKNET_GPU_BRANCH = "yolo34py-intergration-nocv-v2"
DARKNET_CPU_BRANCH = "yolo34py-intergration-nogpu-v2"
DARKNET_URL_SPEC = 'https://github.com/madhawav/darknet/archive/{branch}.zip'
DEFAULT_CUDA_LOCATION = "/usr/local/cuda"

PACKAGE_NAME_GPU = "yolo34py-gpu"
PACKAGE_NAME_CPU = "yolo34py"


class Params:
    """
    Configuration used by the setup script.
    """

    def __init__(self):
        """
        Initialize to default configuration
        """
        self.__use_gpu = False
        self.__use_cv = False
        self.__cuda_home = DEFAULT_CUDA_LOCATION
        self.__darknet_home = None

        self.__darknet_download_required = True

    @property
    def darknet_download_required(self):
        """
        Specify whether a darknet download is required.
        """
        return self.__darknet_download_required

    @darknet_download_required.setter
    def darknet_download_required(self, value):
        if not isinstance(value, bool):
            raise TypeError()
        self.__darknet_download_required = value

    @property
    def darknet_home(self):
        """
        Location of darknet sources
        """
        return self.__darknet_home

    @darknet_home.setter
    def darknet_home(self, value):
        if not isinstance(value, str):
            raise TypeError()
        self.__darknet_home = value

    @property
    def cuda_home(self):
        """
        Location of CUDA. Usually /usr/local/cuda
        """
        return self.__cuda_home

    @cuda_home.setter
    def cuda_home(self, value):
        if not isinstance(value, str):
            raise TypeError()

        if not osp.exists(self.cuda_home):
            raise Exception("Unable to locate CUDA installation. Please specify CUDA_HOME environment variable.")
        self.__cuda_home = value

    @property
    def use_gpu(self):
        """
        Specify whether GPU/CUDA is enabled.
        """
        return self.__use_gpu

    @use_gpu.setter
    def use_gpu(self, value):
        if not isinstance(value, bool):
            raise TypeError()
        self.__use_gpu = value

    @property
    def use_cv(self):
        """
        Specify whether OpenCV is enabled.
        """
        return self.__use_cv

    @use_cv.setter
    def use_cv(self, value):
        if not isinstance(value, bool):
            raise TypeError()

        if value:
            if get_libs("opencv") is None or get_cflags("opencv") is None:
                raise Exception("OpenCV is not configured with pkg-config.")
        self.__use_cv = value

    @property
    def darknet_branch_name(self):
        """
        Retrieve the darknet branch used for download.
        """
        if self.use_gpu and self.use_cv:
            return DARKNET_GPU_OPENCV_BRANCH
        elif self.use_gpu and not self.use_cv:
            return DARKNET_GPU_BRANCH
        elif not self.use_gpu and self.use_cv:
            raise Exception("OpenCV requires GPU branch.")
        elif not self.use_gpu and not self.use_cv:
            return DARKNET_CPU_BRANCH

    @property
    def darknet_url(self):
        """
        Retrieve the URL used to download darknet.
        """
        return DARKNET_URL_SPEC.format(branch=self.darknet_branch_name)

    def verify(self):
        """
        Verify whether params are valid.
        """
        if not self.use_gpu and self.use_cv:
            raise Exception("GPU not used. OpenCV requires GPU enabled.")

    @classmethod
    def load_params(cls):
        """
        Load params from the environment variables.
        """
        params = Params()
        # Load GPU params
        if "CUDA_HOME" in os.environ:
            params.cuda_home = os.environ["CUDA_HOME"]

        if "GPU" in os.environ and int(os.environ["GPU"]) == 1:
            logging.info("Compiling wrapper with gpu")
            params.use_gpu = True
        elif "GPU" in os.environ and int(os.environ["GPU"]) == 0:
            logging.info("Compiling wrapper without gpu")
            params.use_gpu = False

        # Load OpenCV params
        if "OPENCV" in os.environ and int(os.environ["OPENCV"]) == 0:
            logging.info("Compiling wrapper without OpenCV")
            params.use_cv = False
        elif "OPENCV" in os.environ and int(os.environ["OPENCV"]) == 1:
            params.use_cv = True
            logging.info("Compiling wrapper with OpenCV")

        # Load darknet location
        if "DARKNET_HOME" in os.environ:
            params.darknet_home = os.environ["DARKNET_HOME"]
            params.darknet_download_required = False
            logging.info("Using darknet from " + os.environ["DARKNET_HOME"])
        else:
            logging.info(
                "Darknet will be downloaded from '{source}'".format(source=params.darknet_url))
            params.darknet_home = os.path.join(tempfile.gettempdir(), "darknet")  # Temporary directory to build darknet
            params.darknet_download_required = True

        params.verify()
        return params
