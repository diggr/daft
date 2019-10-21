import zipfile
import json
import pandas as pd
import diggrtoolbox as dt
from .utils import get_prov

class MediaartData(object):

    def __init__(self, filepath):
        self._pm = dt.PlatformMapper("mediaartdb")

        self._filepath = filepath
        df = pd.read_csv(filepath, sep="\t")
        data = json.loads(df.to_json(orient="records"))
        self._dict = { str(x["正式ID"]): x for x in data }

    def all_ids(self):
        return list(self._dict.keys())

    def _get_dataset(self, raw):
        id_ = raw["正式ID"]
        title = raw["ゲームタイトル"]
        alt_titles = list(set([ raw["英語表記"], raw["JM（ローマ字）"] ]))
        platforms = [ self._pm.std(raw["プラットフォーム"])]      

        try:
            years = [ int(raw["発売年"]) ]
        except:
            years = []

        genres = [
            raw["ジャンル1"],
            raw["ジャンル2"],
            raw["ジャンル3"],
            raw["ジャンル4"],
            raw["ジャンル5"]
        ]
        

        dataset = {
            "id": id_,
            "raw": raw,
            "title": title,
            "alt_titles": alt_titles,
            "platforms": platforms,
            "years": years,
            "genres": [ g for g in genres if g and g != "-" ]
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

    def prov(self):
        return get_prov(self._filepath)
        