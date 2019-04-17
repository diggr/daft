import json
import diggrtoolbox as dt

class MobygamesData(object):

    def __init__(self, filepath):
        self._filepath = filepath

        self._pm =  dt.PlatformMapper("mobygames")
        self.zipfile = dt.ZipListAccess(filepath)

        self.slug_dict = {}

        for filename in self.zipfile.z.namelist():
            data = self.zipfile[filename]
            self.slug_dict[data["moby_url"].split("/")[-1]] = str(data["game_id"])

    def all_ids(self):
        files = self.zipfile.z.namelist()
        return [ f.replace(".json","") for f in files ]

    def _get_dataset(self, raw):
        id_ = raw["game_id"]
        title = raw["title"]
        alt_titles = [ x["title"] for x in raw["alternate_titles"] ] 
        platforms = [ self._pm.std(x["platform_name"]) for x in raw["platforms"] ]

        years = []
        for platform in raw["platforms"]:
            for release in platform["releases"]:
                if release["release_date"]:
                    years.append(int(release["release_date"][:4]))

        genres = [ g["genre_name"] for g in raw["genres"] ]

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

    def get_item_by_slug(self, slug):
        return self[self.slug_dict[slug]]
        