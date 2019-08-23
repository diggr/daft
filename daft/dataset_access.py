from .reader import get_dataset
from .config import load_config

class DatasetAccess(object):

    def __init__(self):

        config = load_config()

        self._ds = {}

        if config["api"]:
            for dataset in config["api"]:
                self._ds[dataset] = get_dataset(".", dataset)


    def __getitem__(self, item):
        return self._ds[item]

def load_datasets():
    return DatasetAccess()