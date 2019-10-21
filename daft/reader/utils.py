import os
import json 

def get_prov(filepath):
    prov_filepath = str(filepath) + ".prov"
    prov_data = {}
    if os.path.exists(prov_filepath):
        with open(prov_filepath) as f:
            prov_data = json.loads(f.read())
    return prov_data