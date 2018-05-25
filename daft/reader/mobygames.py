import zipfile
import json
from ..utils.platform_mapper import PlatformMapper

PM_FILE = "/home/pmuehleder/data/game_metadata/platform_mapping/mobygames.csv"

class MobygamesData(object):

    def __init__(self, filepath):
        self._filepath = filepath
        self._pm = PlatformMapper(PM_FILE, sep=";")

    def _get_dataset(self, raw):
        id_ = raw["game_id"]
        title = raw["title"]
        alt_titles = [ x["title"] for x in raw["alternate_titles"] ] 
        platforms = [ self._pm.std(x["platform_name"]) for x in raw["platforms"] ]

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
        with zipfile.ZipFile(self._filepath) as zf:
            filename = "{}.json".format(id_)
            with zf.open(filename) as f:
                data_string = f.read().decode("utf-8")
                data = json.loads(data_string)
                return self._get_dataset(data)

    def __iter__(self):
        """
        Iterator over mobygames dataset
        """
        with zipfile.ZipFile(self._filepath) as zf:
            for filename in zf.namelist():
                with zf.open(filename) as f:
                    data_string = f.read().decode("utf-8")
                    data = json.loads(data_string)
                    yield self._get_dataset(data)

    def source_file(self):
        return self._filepath
        