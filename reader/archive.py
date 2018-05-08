import zipfile
import json

def read_archive(zipfilename):
    """
    Reads archive zipfile and returns contents as list of dicts.
    """
    zipfilename = zipfilename
    object_list = []

    with zipfile.ZipFile(zipfilename) as zf:
        for filename in zf.namelist():
            with zf.open(filename) as f:
                data = f.read().decode("utf-8")
                object_list.append(data)
    return object_list

