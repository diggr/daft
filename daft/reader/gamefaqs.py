import zipfile
import json
from ..utils.platform_mapper import PlatformMapper

PM_FILE = "/home/pmuehleder/data/game_metadata/platform_mapping/gamefaqs.csv"

class GamefaqsData(object):

    def __init__(self, filepath):
        self._filepath = filepath
        self._pm = PlatformMapper(PM_FILE, sep=";")
        data = json.load(open(filepath))
        self._dict = { str(x["_id"]).replace("/","__"): x for x in data }


    def _get_dataset(self, raw):
        id_ = raw["_id"].replace("/","__")
        title = raw["data"]["title"]
        alt_titles = list(set([ x["title"] for x in  raw["data"]["releases"] ] ))
        if title in alt_titles:
            alt_titles.remove(title)
        platforms = [ self._pm.std(raw["platform"]) ]

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
        return self._get_dataset(self._dict[_id])

    def __iter__(self):
        """
        Iterator over mobygames dataset
        """
        for id_, entry in self._dict.items():
            yield self._get_dataset(entry)

    def source_file(self):
        return self._filepath
        