import json
import requests
import os
import zipfile
from pit.prov import Provenance

from .utils import timeout


URL = "https://www.giantbomb.com/api/games/?api_key={api_key}&format=json&offset={offset}"

OFFSET_STEP = 100
TIMEOUT = 1

HEADERS = {'User-agent': 'daft fetcher'}

class GiantbombFetcher(object):
    """
    wrapper class for giantbomb api.

    Attributes:
        api_key: Api key for mobygames api
        data_dir: data directory
        filepath: location of mobygames archive zip file
    """

    def __init__(self, api_key, data_dir):
        """setting up api key and proxies"""
        self.data_dir = data_dir
        self.filepath = os.path.join(data_dir, "giantbomb.zip")
        self.api_key = api_key

    @timeout(TIMEOUT)
    def _api_call(self, url):
        """
        Calls Mobygames API, returns json as dict
        """
        resp = requests.get(url, headers=HEADERS)
        return json.loads(resp.text)


    def _read_from_archive(self, zf, id_):
        """
        Checks if game :id_: is in archive; if not returns None
        """
        try:
            with zf.open("{}.json".format(id_)) as f:
                data = json.load(f)
            return data
        except KeyError:
            return None

    def update(self):
        """
        WIP - not clear if it's an endeavour worth pursuing
        """
        if not os.path.exists(self.filepath):
            print("Archive file  does not exits, fetch full dataset")
            self.fetch()
            return 

        with zipfile.ZipFile(self.filepath, "a", zipfile.ZIP_DEFLATED) as zf:            

            offset = 0          
            while True:

                result = self._api_call(URL.format(api_key=self.api_key, title="", offset=offset))
                
                games = result["results"]
                for game in games:
                    id_ = game["guid"]
                    last_update = game["date_last_updated"] 
                    data = self._read_from_archive(zf, id_)

                    if data:
                        if last_update > data["date_last_updated"]:
                            print("newer")
                        else:
                            print("older or equal")

                    break
                break



    def fetch(self):
        """
        Fetches all mobygames datasets and write the file />data_dir>/mobygames.zip
        """          
        with zipfile.ZipFile(self.filepath, "w", zipfile.ZIP_DEFLATED) as zf:

            offset = 0          
            while True:
                result = self._api_call(URL.format(api_key=self.api_key, title="", offset=offset))
               
                games = result["results"]
                for game in games:
                    game_str = json.dumps(game, indent=4)
                    zf.writestr("{}.json".format(game["guid"]), game_str)

                offset += OFFSET_STEP
                result_number = len(games)
                print(offset)

                if result_number == 0:
                    break
                
        prov = Provenance(self.filepath)
        prov.add(agent="daft", activity="fetch_giantbomb", description="fetches all game datasets from giantbomb api")
        prov.add_primary_source("giantbomb")
        prov.save()
