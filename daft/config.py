"""
Handles daft configuration

initialize() creates a config.yml template in the current directory

load_config() loads configuration file

"""


import yaml
import os

PROV_AGENT = "daft_1.0.0"

CONFIG_TEMPLATE = """
project:
  name: ""
  data_dir: ""
  export_dir: ""

sources:
  mobygames:
    api_key: ""

api: #add datasets to api
#- mobygames

export: #define dataset exports
#  mobygames:
#      - title
#      - alt_titles
#      - platforms
#      - genres
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
    config = yaml.safe_load(open("config.yml"))

    if not os.path.exists(config["project"]["data_dir"]):
        os.makedirs(config["project"]["data_dir"])
    if not os.path.exists(config["project"]["export_dir"]):
        os.makedirs(config["project"]["export_dir"])

    return config

