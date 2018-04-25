"""
daft - video game metadata fetcher command line tool

use:

# create config.yml
daft --init

# fetch full dataset
daft <source> --fetch

# update dataset (if available)
daft <source> --update

"""

import click

from fetcher.config import initialize, load_config
from fetcher.mobygames import MobygamesFetcher
from fetcher.giantbomb import GiantbombFetcher


@click.command()
@click.argument("source", required=False)
@click.option("--init", "-i", is_flag=True, help="Create config.yml template")
@click.option("--fetch", "-f", is_flag=True, help="Fetch full dataset from source")
@click.option("--update", "-u", is_flag=True, help="Fetch update from data source (if available)")
def daft_tool(source, fetch, update, init):

    config, datasets = load_config()

    if init:
        initialize()

    if source == "mobygames":
        mobygames = MobygamesFetcher(data_dir=config["data_dir"], api_key=datasets["mobygames"]["api_key"])
        if fetch:
            mobygames.fetch()
    
    if source == "giantbomb":
        giantbomb = GiantbombFetcher(data_dir=config["data_dir"], api_key=datasets["giantbomb"]["api_key"])
        if fetch:
            giantbomb.fetch()
        if update:
            giantbomb.update()

    if source == "punk":
        print("5555")