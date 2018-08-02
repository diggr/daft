import json
#from ..utils.platform_mapper import PlatformMapper
import diggrtoolbox as dt

#PM_FILE = "/home/pmuehleder/data/game_metadata/platform_mapping/mobygames.csv"

class MobygamesData(object):

    def __init__(self, filepath):
        self._filepath = filepath

        self._pm =  dt.PlatformMapper("mobygames")
        self.zipfile = dt.ZipListAccess(filepath)

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
        filename = "{}.json".format(id_)
        data = self.zipfile[filename]
        return self._get_dataset(data)

    def __iter__(self):
        """
        Iterator over mobygames dataset
        """
        for data in self.zipfile:
            yield self._get_dataset(data)

    def source_file(self):
        return self._filepath
        