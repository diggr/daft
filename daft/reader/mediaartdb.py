import zipfile
import json
import pandas as pd
from ..utils.platform_mapper import PlatformMapper

PM_FILE = "/home/pmuehleder/data/game_metadata/platform_mapping/mediaartdb.csv"


class MediaartData(object):

    def __init__(self, filepath):
        self._pm = PlatformMapper(PM_FILE, sep=";")

        self._filepath = filepath
        df = pd.read_csv(filepath, sep="\t")
        data = json.loads(df.to_json(orient="records"))
        self._dict = { str(x["正式ID"]): x for x in data }

    def _get_dataset(self, raw):
        id_ = raw["正式ID"]
        title = raw["ゲームタイトル"]
        alt_titles = list(set([ raw["英語表記"], raw["JM（ローマ字）"] ]))
        platforms = [ self._pm.std(raw["プラットフォーム"])]        

        dataset = {
            "id": id_,
            "raw": raw,
            "title": title,
            "alt_titles": alt_titles,
            "platforms": platforms
        }
        return dataset

    def __getitem__(self, id_):
        """
        Returns mobygames dataset with id :id_:
        """
        return self._get_dataset(self._dict[id_])

    def __iter__(self):
        """
        Iterator over mobygames dataset
        """
        for id_, entry in self._dict.items():
            yield self._get_dataset(entry)

    def source_file(self):
        return self._filepath
        