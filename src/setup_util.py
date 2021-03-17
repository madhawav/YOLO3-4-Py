import shlex
import subprocess
import os
import zipfile
import shutil
import logging
import sys

darknet_setup_done = False  # Guard to avoid repeated building of darknet.

logging.basicConfig(level=logging.INFO)


def setup_darknet(target_location, download_darknet, darknet_dir, darknet_url, build_branch_name):
    """
    Locates compiled darknet and moves it to target_location. Download and compile darknet if required.
    """
    global darknet_setup_done
    if darknet_setup_done:
        return

    if download_darknet:
        # If user has not specified DARKNET_HOME, we will download and build darknet.
        build_darknet(darknet_dir, darknet_url, build_branch_name)
        logging.info("Moving to " + target_location)
        shutil.move(os.path.join(darknet_dir, "darknet-" + build_branch_name + "/libdarknet.so"), target_location)
    else:
        logging.info("Copying libdarknet.so from " + darknet_dir)
        # If user has set DARKNET_HOME, it is assumed that he has built darknet.
        # We will copy libdarknet.so from users location to site-pacakges/__libdarknet
        shutil.copyfile(os.path.join(darknet_dir, "libdarknet.so"),
                        target_location)

    darknet_setup_done = True


def build_darknet(download_path, darknet_url, branch_name):
    """
    Utility method to download and build darknet
    :param download_path: Path to download darknet sources
    :param branch_name: Branch of darknet used.
    :return:
    """
    import requests  # Used to download darknet
    logging.info("Temp Path: " + download_path)

    logging.info("Downloading darknet")
    os.makedirs(download_path, exist_ok=True)
    response = requests.get(darknet_url)

    logging.info("Extracting darknet")
    with open(os.path.join(download_path, "darknet.zip"), "wb") as f:
        f.write(response.content)

    zip_ref = zipfile.ZipFile(os.path.join(download_path, "darknet.zip"), 'r')
    zip_ref.extractall(download_path)
    zip_ref.close()

    os.remove(os.path.join(download_path, "darknet.zip"))

    logging.info("Building darknet")
    build_ret = subprocess.Popen("make", shell=True, stdout=subprocess.PIPE,
                                 cwd=os.path.join(download_path, "darknet-" + branch_name))

    for line in iter(build_ret.stdout.readline, ''):
        if len(line) != 0:
            logging.info(line.rstrip())
        else:
            break

    if build_ret.wait() == 0:
        logging.info("Darknet building successful")
    else:
        return False

    return True


def clean_darknet(darknet_path):
    """
    Cleanup darknet download
    :param darknet_path:
    :return:
    """
    shutil.rmtree(darknet_path, ignore_errors=True)


def get_python_cflags():
    """
    Utility method to retrieve compiler flags to compile a python library. Uses 'python3-config --cflags'.
    """
    command = "python3-config --cflags"
    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    return out.rstrip().decode('utf-8').split()


def get_python_libs():
    """
    Utility method to retrieve linker flags to build a python library. Uses 'python3-config --libs'.
    """
    command = "python3-config --libs"
    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    return out.rstrip().decode('utf-8').split()


def get_readme():
    """
    Retrieve readme of the package.
    """
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pypi_readme.md"), "r") as f:
        return f.read()


# Code based on https://github.com/matze/pkgconfig
def get_cflags(package):
    """
    Retrieve cflags of a package using pkg-config.
    """

    call_name = "pkg-config"
    if 'PKG_CONFIG' in os.environ:
        call_name = os.environ['PKG_CONFIG']

    command = call_name + " --cflags " + package

    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    response = out.rstrip().decode('utf-8').split()
    if len(response) == 0:
        return None
    return response


def find_site_packages():
    """
    Retrieve site-packages directories.
    """

    site_packages = [p for p in sys.path if p.endswith("site-packages") or p.endswith("site-packages/")]
    return site_packages


def find_dist_packages():
    """
    Retrieve dist-packages directories.
    """

    dist_packages = [p for p in sys.path if p.endswith("dist-packages") or p.endswith("dist-packages/")]
    return dist_packages


def get_libs(package):
    """
    Retrieve libs of a package using pkg-config.
    """

    call_name = "pkg-config"
    if 'PKG_CONFIG' in os.environ:
        call_name = os.environ["PKG_CONFIG"]

    command = call_name + " --libs " + package

    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    response = out.rstrip().decode('utf-8').split()
    if len(response) == 0:
        return None
    return response
