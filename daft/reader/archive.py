import zipfile
import json

def read_archive(zipfilename):
    """
    Reads archive zipfile and returns contents as list of dicts.
    """
<<<<<<< HEAD
    filepath = filepath
    
    games = {}
    with zipfile.ZipFile(filepath) as zf:
        for filename in zf.namelist():
            with zf.open(filename) as f:
                data = f.read().decode("utf-8")
                games[filename.replace(".json", "").strip()] = json.loads(data)
    return games
            
=======
    zipfilename = zipfilename
    object_list = []

    with zipfile.ZipFile(zipfilename) as zf:
        for filename in zf.namelist():
            with zf.open(filename) as f:
                data = f.read().decode("utf-8")
                object_list.append(data)
    return object_list

>>>>>>> 8a3e4a51055546db3c0be453efc836b1e2764648
