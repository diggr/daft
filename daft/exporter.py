import os
import json
from provit import Provenance
from .reader import get_dataset
from .config import load_config, PROV_AGENT

def export_datasets():
    """
    Exports standardized datasets with fields spezified in the config.yml
    """
    config = load_config()

    for dataset_name, fields in config["export"].items():
        export_dataset = {}
        
        print("exporting dataset <{}> ...".format(dataset_name))
        dataset = get_dataset(".", dataset_name)

        for entry in dataset:
            row = { field: entry[field] for field in fields }
            row["id"] = entry["id"]
            export_dataset[entry["id"]] = row

        out_file = os.path.join(config["project"]["export_dir"], "{}.json".format(dataset_name))
        json.dump(export_dataset, open(out_file, "w"), indent=4)

        prov = Provenance(out_file, overwrite=True)
        prov.add(
            agents=[ PROV_AGENT ], 
            activity="export_std_dataset",
            description="export standardized fields <{}> from dataset <{}>".format(", ".join(fields), dataset_name)
        )
        prov.add_sources(dataset.source_file())
        prov.save()

