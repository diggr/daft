import yaml
import os

CONFIG_TEMPLATE = """
project:
  name: ""
  data_directory: ""

datasets:
  mobygames:
    api_key: ""
  giantbomb:
    api_key: ""
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
    Reads config yml; returns config options :config: and dataset config :datsets:
    """
    if not os.path.exists("config.yml"):
        raise IOError("config.yml does not exits. Initialize it with 'daft init' ")

    config = {}
    config_yml = yaml.load(open("config.yml"))
    config["project_name"] = config_yml["project"]["name"]
    config["data_dir"] = config_yml["project"]["data_directory"]

    if not os.path.exists(config["data_dir"]):
        os.makedirs(config["data_dir"])
    
    datasets = {}
    datasets["mobygames"] = { "api_key": config_yml["datasets"]["mobygames"]["api_key"] }
    datasets["giantbomb"] = { "api_key": config_yml["datasets"]["giantbomb"]["api_key"] }

    return config, datasets

