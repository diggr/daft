import os
import yaml
from .mediaartdb import MediaartData
from .mobygames import MobygamesData, MobygamesCompany
from .gamefaqs import GamefaqsData

def load_config_file(directory):
    config_filepath = os.path.join(directory, "config.yml")
    if os.path.exists(config_filepath):
        config = yaml.safe_load(open(config_filepath))
        return config
    else:
        return None

      

def get_dataset(daft_dir, dataset_name):

    config = load_config_file(daft_dir)
    if config:
        data_dir = os.path.join(daft_dir, 
                            config["project"]["data_dir"])

        if dataset_name == "mobygames":
            return MobygamesData(os.path.join(data_dir, "mobygames.zip"))
        if dataset_name == "mediaartdb":
            return MediaartData(os.path.join(data_dir, "ma_master_u8.csv"))
        if dataset_name == "gamefaqs":
            return GamefaqsData(os.path.join(data_dir, "gamefaqs.json"))

        if dataset_name == "mobygames-companies":
            slug_mapping = os.path.join(data_dir, "mobygames_companies_id_to_slug.json")
            company_dataset = os.path.join(data_dir, "mobygames_companies.json")
            return MobygamesCompany(company_dataset, slug_mapping)