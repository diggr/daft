import pandas as pd
import json

class PlatformMapper(object):

    def __init__(self, filepath, sep=","):
        df = pd.read_csv(filepath, sep=sep)
        self.mapping = json.loads(df.to_json(orient="records"))

        self.mapping_dict = { x["source"]:x["diggr"] for x in self.mapping if x["diggr"] }

    def std(self, source_name):
        if source_name in self.mapping_dict:
            return self.mapping_dict[source_name].strip()
        else:
            return None