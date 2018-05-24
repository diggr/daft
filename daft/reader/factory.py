import os
import yaml
from .mediaartdb import MediaartData
from .mobygames import MobygamesData

def load_config_file(directory):
    config_filepath = os.path.join(directory, "config.yml")
    config = yaml.load(open(config_filepath))
    return config

def get_dataset(daft_dir, dataset_name):

    config = load_config_file(daft_dir)
    data_dir =os.path.join(daft_dir, 
                           config["project"]["data_directory"])

    if dataset_name == "mobygames":
        return MobygamesData(os.path.join(data_dir, "mobygames.zip"))
    if dataset_name == "mediaartdb":
        return MediaartData(os.path.join(data_dir, "ma_master_u8.csv"))