from reader.archive import read_archive
import pandas as pd
import os
import json
from tqdm import tqdm
from pit.prov import Provenance
from utils.platform_mapper import PlatformMapper

EXPORT_DIR = "/home/pmuehleder/data/game_metadata/daft_export"

PM_DIR = "/home/pmuehleder/data/game_metadata/platform_mapping"

def main():
    
    #mobygames export
    print("export mobygames games ...")

    input_filepath = "data/mobygames.zip"

    pm = PlatformMapper(os.path.join(PM_DIR, "mobygames.csv"), sep=";")

    mobygames = read_archive(input_filepath)
    export = {}
    for game in tqdm(mobygames):
        try:
            aliases = game["alternative_titles"]
        except:
            aliases = []

        try:
            platforms = [ x["platform_name"] for x in game["platforms"] ]
        except:
            platforms = []

        platforms = [ pm.std(x) for x in platforms ]

        export[game["game_id"]] = {
            "giantbomb_id": game["game_id"],
            "name": [ game["title"] ] + aliases,
            "platforms": [x for x in platforms if x ]
        }
    export_filename = os.path.join(EXPORT_DIR, "mobygames.json")
    json.dump(export, open(export_filename, "w"), indent=4)

    prov = Provenance(export_filename)
    prov.add(agent="daft", activity="linking_export", description="standardized mobygames export for dataset linking")
    prov.add_sources([ input_filepath ])
    prov.save()


    #giantbomb export
    print("export giantbomb games ...")

    input_filepath = "data/giantbomb.zip"

    pm = PlatformMapper(os.path.join(PM_DIR, "giantbomb.csv"))

    giantbomb = read_archive(input_filepath)
    export = {}
    for game in tqdm(giantbomb):
        try:
            aliases = [ x.strip() for x in game["aliases"].split("\n") if x.strip() != "" ]
        except:
            aliases = []

        try:
            platforms = [ x["name"] for x in game["platforms"] ]
        except:
            platforms = []

        platforms = [ pm.std(x) for x in platforms ]

        export[game["guid"]] = {
            "giantbomb_id": game["guid"],
            "name": [ game["name"] ] + aliases,
            "platforms": [x for x in platforms if x ]
        }
    export_filename = os.path.join(EXPORT_DIR, "giantbomb.json")
    json.dump(export, open(export_filename, "w"), indent=4)

    prov = Provenance(export_filename)
    prov.add(agent="daft", activity="linking_export", description="standardized giantbomb export for dataset linking")
    prov.add_sources([ input_filepath ])
    prov.save()

    print(len(giantbomb))



    #wikidata export
    print("export wikidata games ...")

    input_filepath = "data/wikidata_games.json"
    wikidata = json.load(open(input_filepath))
    export = {}
    for game in tqdm(wikidata):
        wkp = game["game"].split("/")[-1]
        if wkp in export:
            if "label_en" in game:
                export[wkp]["label_en"].add(game["label_en"])
            if "label_ja" in game:
                export[wkp]["label_ja"].add(game["label_ja"])
            if "label_de" in game:
                export[wkp]["label_de"].add(game["label_de"])
            export[wkp]["platforms"].add(game["platform_label"])
        else:
            export[wkp] = {
                "wkp": game["game"],
                "label_en": set(),
                "label_ja": set(),
                "label_de": set(),
                "platforms": set()
            }
            if "label_en" in game:
                export[wkp]["label_en"].add(game["label_en"])
            if "label_ja" in game:
                export[wkp]["label_ja"].add(game["label_ja"])
            if "label_de" in game:
                export[wkp]["label_de"].add(game["label_de"])
            export[wkp]["platforms"].add(game["platform_label"])
    
    pm = PlatformMapper(os.path.join(PM_DIR, "wikidata.csv"))
    for wkp, game in export.items():
        game["label_en"] = list(game["label_en"])
        game["label_ja"] = list(game["label_ja"])
        game["label_de"] = list(game["label_de"])
        platforms = [ pm.std(x) for x in game["platforms"] ]
        game["platforms"] = [ x for x in platforms if x ]

    export_filename = os.path.join(EXPORT_DIR, "wikidata.json")
    json.dump(export, open(export_filename, "w"), indent=4)    

    prov = Provenance(export_filename)
    prov.add(agent="daft", activity="linking_export", description="standardized wikidata export for dataset linking")
    prov.add_sources([ input_filepath ])
    prov.save()
    




if __name__ == "__main__":
    main()