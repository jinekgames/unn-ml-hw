import os
import shutil
import urllib.request
import zipfile

from config import DATA_DIR

def __RenameCsv(fiename: str) -> str:
    newFilepath = os.path.join(DATA_DIR, "dataset.csv")
    os.rename(fiename, newFilepath)
    return newFilepath

def DowloadData(url: str) -> str:
    # url: download link for .csv or .zip

    if os.path.isdir(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    os.mkdir(DATA_DIR)

    loadedFilename, headers = urllib.request.urlretrieve(url, os.path.join(DATA_DIR, "dataset.zip"))
    if not os.path.isfile(loadedFilename):
        print("Error: failed to dowload dataset")
        return ""

    try:
        zip_ref = zipfile.ZipFile(loadedFilename, 'r')
    except zipfile.BadZipFile:
        ret = __RenameCsv(loadedFilename)
        return ret

    with zipfile.ZipFile(loadedFilename, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)
    files = os.listdir(DATA_DIR)
    for file in files:
        filename, file_extension = os.path.splitext(file)
        filepath = os.path.join(DATA_DIR, file)
        if file_extension == ".csv":
            ret = __RenameCsv(filepath)
            os.remove(loadedFilename)
            return ret
    print("Error: failed unzip dataset")
    return ""
