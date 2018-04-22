import subprocess
import os
import requests
import zipfile
import shutil

def build_darknet(darknet_dir):
    '''
    Utility method to download and install darknet
    :param download_path:
    :return:
    '''
    download_path = darknet_dir
    print("Temp Path:", download_path)

    print("Downloading darknet")
    os.makedirs(download_path, exist_ok=True)
    response = requests.get('https://github.com/madhawav/darknet/archive/yolo34py-intergration.zip')

    print("Extracting darknet")
    with open(os.path.join(download_path,"darknet.zip"), "wb") as f:
        f.write(response.content)

    zip_ref = zipfile.ZipFile(os.path.join(download_path,"darknet.zip"), 'r')
    zip_ref.extractall(download_path)
    zip_ref.close()

    os.remove(os.path.join(download_path, "darknet.zip"))

    print("Building darknet")
    build_ret = subprocess.Popen("make", shell=True, stdout=subprocess.PIPE, cwd=os.path.join(download_path,"darknet-yolo34py-intergration"))
    if build_ret.wait() == 0:
        print("Darknet building successful")
    else:
        return False

    print("Moving to __libdarknet/")
    shutil.move(os.path.join(download_path,"darknet-yolo34py-intergration/libdarknet.so"), os.path.join(os.path.dirname(__file__),"__libdarknet","libdarknet.so"))

    return True

def clean_darknet(darknet_path):
    '''
    Cleanup darknet download
    :param darknet_path:
    :return:
    '''
    shutil.rmtree(darknet_path,ignore_errors=True)
