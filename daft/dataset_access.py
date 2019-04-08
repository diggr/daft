from .reader import get_dataset

class DatasetAccess(object):

    def __init__(self):
        self._ds = {
            "mobygames": get_dataset(".","mobygames"),
            "gamefaqs": get_dataset(".", "gamefaqs"),
            "mediaartdb": get_dataset(".", "mediaartdb")
        }

    def __getitem__(self, item):
        return self._ds[item]

def load_datasets():
    return DatasetAccess()