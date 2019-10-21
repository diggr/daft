import json
import os
import diggrtoolbox as dt
from .utils import get_prov

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

    def _get_data(self, id):
        pass

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

    def get_companies(self, game_id):
        companies = []
        raw = self[game_id]["raw"]
        for platform in raw["platforms"]:
            for release in platform["releases"]:
                for company in release["companies"]:
                    company["release_countries"] = release["countries"]
                    company["platform"] = self._pm.std(platform["platform_name"])
                    companies.append(company)
        return companies

    def prov(self):
        return get_prov(self._filepath)




class MobygamesCompany(object):

    def __init__(self, company_dataset_filepath, slug_mapping_filepath):

        self._filepath = company_dataset_filepath

        with open(company_dataset_filepath) as f:
            self.companies = json.load(f)

        with open(slug_mapping_filepath) as f:
            data = json.load(f)
            self.id_2_slug = { x["company_id"]: x["slug"] for x in data }
    
    def id2slug(self):
        pass

    def __getitem__(self, id_):
        return self.companies[id_]

    def prov(self):
        return get_prov(self._filepath)    