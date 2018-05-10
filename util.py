import shlex
import subprocess
import os
import zipfile
import shutil
import logging
import sys

logging.basicConfig(level=logging.INFO)

def build_darknet(darknet_dir, branch_name, target_location):
    '''
    Utility method to download and install darknet
    :param download_path:
    :return:
    '''
    import requests
    download_path = darknet_dir
    logging.info("Temp Path: "+ download_path)

    logging.info("Downloading darknet")
    os.makedirs(download_path, exist_ok=True)
    response = requests.get('https://github.com/madhawav/darknet/archive/'+branch_name+'.zip')

    logging.info("Extracting darknet")
    with open(os.path.join(download_path,"darknet.zip"), "wb") as f:
        f.write(response.content)

    zip_ref = zipfile.ZipFile(os.path.join(download_path,"darknet.zip"), 'r')
    zip_ref.extractall(download_path)
    zip_ref.close()

    os.remove(os.path.join(download_path, "darknet.zip"))

    logging.info("Building darknet")
    build_ret = subprocess.Popen("make", shell=True, stdout=subprocess.PIPE, cwd=os.path.join(download_path,"darknet-"+branch_name))

    for line in iter(build_ret.stdout.readline, ''):
        if len(line) != 0:
            logging.info(line.rstrip())
        else:
            break

    if build_ret.wait() == 0:
        logging.info("Darknet building successful")
    else:
        return False

    logging.info("Moving to " + target_location)
    shutil.move(os.path.join(download_path,"darknet-"+branch_name+"/libdarknet.so"), target_location)

    return True

def clean_darknet(darknet_path):
    '''
    Cleanup darknet download
    :param darknet_path:
    :return:
    '''
    shutil.rmtree(darknet_path,ignore_errors=True)


# Code based on https://github.com/matze/pkgconfig
def get_cflags(package):
    call_name = "pkg-config"
    if 'PKG_CONFIG' in os.environ:
        call_name = "pkg-config"

    command = call_name + " --cflags " + package

    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    return out.rstrip().decode('utf-8')


def find_site_packages():
    site_packages = [p for p in sys.path if p.endswith("site-packages") or p.endswith("site-packages/")]
    return site_packages

def find_dist_packages():
    dist_packages = [p for p in sys.path if p.endswith("dist-packages") or p.endswith("dist-packages/")]
    return dist_packages

def get_libs(package):
    call_name = "pkg-config"
    if 'PKG_CONFIG' in os.environ:
        call_name = "pkg-config"

    command = call_name + " --libs " + package

    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    return out.rstrip().decode('utf-8')

def get_readme():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"pypi_readme.md"),"r") as f:
        return f.read()