from daft.reader.archive import read_archive
import pandas as pd
import os
import json

EXPORT_DIR = "/home/pmuehleder/data/game_metadata/platform_mapping"



def main():
    input_filepath = "data/giantbomb.zip"
    giantbomb = read_archive(input_filepath)
    platforms = []
    for game in giantbomb:
        #print(game)
        if game["platforms"]:
            platforms += [ x["name"] for x in game["platforms"]  ]
    
    platforms = sorted(list(set(platforms)))
    platforms = [ { "GIANTBOMB": x, "PlatformMap_GIANTBOMB": "" } for x in platforms ]

    export_filepath = os.path.join(EXPORT_DIR, "giantbomb.csv")
    df = pd.DataFrame(platforms)
    df.to_csv(export_filepath, index=False)

    input_filepath = "data/wikidata_games.json"
    wikidata = json.load(open(input_filepath))
    platforms = [ x["platform_label"] for x in wikidata ]
    
    platforms = sorted(list(set(platforms)))
    platforms = [ { "WIKIDATA": x, "PlatformMap_WIKIDATA": "" } for x in platforms ]

    export_filepath = os.path.join(EXPORT_DIR, "wikidata.csv")
    df = pd.DataFrame(platforms)
    df.to_csv(export_filepath, index=False)


if __name__ == "__main__":
    main()