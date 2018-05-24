import os
from .mediaartdb import MediaartData
from .mobygames import MobygamesData

def get_dataset(data_dir, dataset_name):
    if dataset_name == "mobygames":
        return MobygamesData(os.path.join(data_dir, "mobygames.zip"))
    if dataset_name == "mediaart":
        return MediaartData(os.path.join(data_dir, "ma_master_u8.csv"))