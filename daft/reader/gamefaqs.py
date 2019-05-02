import zipfile
import json
import diggrtoolbox as dt
from dateutil.parser import parse

class GamefaqsData(object):

    def __init__(self, filepath):
        self._filepath = filepath
        self._pm = dt.PlatformMapper("gamefaqs")
        data = json.load(open(filepath))
        self._dict = { str(x["_id"]).replace("/","__"): x for x in data }


    def all_ids(self):
        return list(self._dict.keys())

    def _get_dataset(self, raw):
        id_ = raw["_id"].replace("/","__")
        title = raw["data"]["title"]
        alt_titles = list(set([ x["title"] for x in  raw["data"]["releases"] ] ))
        if title in alt_titles:
            alt_titles.remove(title)
        platforms = [ self._pm.std(raw["platform"]) ]

        years = []
        for release  in raw["data"]["releases"]:
            if release["release_date"]:
                try:
                    years.append( parse(release["release_date"], fuzzy=True).year )
                except:
                    continue

        genres = [ raw["data"]["genre"] ]

        dataset = {
            "id": id_,
            "raw": raw,
            "title": title,
            "alt_titles": alt_titles,
            "platforms": platforms,
            "years": list(set(years)),
            "genres": genres
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
        