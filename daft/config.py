"""
Handles daft configuration

initialize() creates a config.yml template in the current directory

load_config() loads configuration file

"""


import yaml
import os

PROV_AGENT = "daft_0.2"

CONFIG_TEMPLATE = """
project:
  name: ""
  data_directory: ""

datasets:
  mobygames:
    api_key: ""
  giantbomb:
    api_key: ""
export:
"""

def initialize():
    """
    Initializes daft project.
    """
    if os.path.exists("config.yml"):
        print("Project already initialized")
        return

    with open("config.yml", "w") as f:
        f.write(CONFIG_TEMPLATE)

def load_config():
    """
    Reads config yml; returns config options :config: and dataset config :datasets:
    """
    if not os.path.exists("config.yml"):
        raise IOError("config.yml does not exits. Initialize it with 'daft init' ")

    config = {}
    config_yml = yaml.safe_load(open("config.yml"))
    config["project_name"] = config_yml["project"]["name"]
    config["data_dir"] = config_yml["project"]["data_directory"]
    config["export_dir"] = config_yml["project"]["export_directory"]
    config["export"] = config_yml["export"]

    if not os.path.exists(config["data_dir"]):
        os.makedirs(config["data_dir"])
    
    datasets = {}
    datasets["mobygames"] = { 
        "api_key": config_yml["datasets"]["mobygames"]["api_key"]
    }
    datasets["giantbomb"] = { 
        "api_key": config_yml["datasets"]["giantbomb"]["api_key"]
    }

    return config, datasets

