import zipfile
import json

def read_archive(filepath):
    """
    Reads archive zipfile and returns contents as list of dicts
    """
    filepath = filepath
    
    games = []
    with zipfile.ZipFile(filepath) as zf:
        for filename in zf.namelist():
            with zf.open(filename) as f:
                games.append(json.load(f))
    return games
            