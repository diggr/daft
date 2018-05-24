import zipfile
import json
import pandas as pd

class MediaartData(object):

    def __init__(self, filepath):
        self._filepath = filepath
        df = pd.read_csv(filepath, sep="\t")
        data = json.loads(df.to_json(orient="records"))
        self._dict = { str(x["正式ID"]): x for x in data }

    def __getitem__(self, id_):
        """
        Returns mobygames dataset with id :id_:
        """
        return self._dict[id_]

    def __iter__(self):
        """
        Iterator over mobygames dataset
        """
        for id_, entry in self._dict.items():
            dataset = {
                "id": id_, 
                "raw": entry
            }
            yield dataset

    def source_file(self):
        return self._filepath
        