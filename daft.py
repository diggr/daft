from mobygames.config import init, load_config
from mobygames.fetcher import MobygamesFetcher


#init()
config, datasets = load_config()
mobygames = MobygamesFetcher(data_dir=config["data_dir"], api_key=datasets["mobygames"]["api_key"])
mobygames.fetch()