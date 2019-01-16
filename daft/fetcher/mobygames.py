import time
import zipfile
import requests
import json
import os
from provit import Provenance
from .utils import timeout
from ..config import PROV_AGENT

# Mobygames API strings
SEARCH = "https://api.mobygames.com/v1/games?format=full&api_key={api_key}&title={title}&offset={offset}"

#Max number of returned games = 5 (when format = full)
OFFSET_STEP = 5

#required timeout for mobygames api: 1 second
TIMEOUT = 1

class MobygamesFetcher:
    """
    wrapper class for mobygames api.

    Attributes:
        api_key: Api key for mobygames api
        data_dir: data directory
        filepath: location of mobygames archive zip file
    """

    def __init__(self, api_key, data_dir):
        """setting up api key and proxies"""
        self.data_dir = data_dir
        self.filepath = os.path.join(data_dir, "mobygames.zip")
        self.api_key = api_key

    @timeout(TIMEOUT)
    def _api_call(self, url):
        """
        Calls Mobygames API, returns json as dict
        """
        resp = requests.get(url)
        return json.loads(resp.text)

    def update(self):
        raise NotImplementedError

    def fetch(self):
        """
        Fetches all mobygames datasets and write the file />data_dir>/mobygames.zip
        """          
        with zipfile.ZipFile(self.filepath, "w", zipfile.ZIP_DEFLATED) as zf:

            offset = 0          
            while True:
            
                result = self._api_call(SEARCH.format(api_key=self.api_key, title="", offset=offset))
                games = result["games"]
                for game in games:
                    game_str = json.dumps(game, indent=4)
                    zf.writestr("{}.json".format(game["game_id"]), game_str)

                offset += OFFSET_STEP
                result_number = len(games)
                print(offset)

                if result_number == 0:
                    break
                
        prov = Provenance(self.filepath)
        prov.add(agent=[ PROV_AGENT ], activity="fetch_mobygames", description="fetches all full game datasets from mobygames api")
        prov.add_primary_source("mobygames")
        prov.save()

