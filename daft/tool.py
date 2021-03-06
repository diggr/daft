#!?usr/bin/env python3
"""
daft -  video game metadata fetcher command line tool

Authors: P.Mühleder <muehleder@ub.uni-leipzig.de>,
         F. Rämisch <raemisch@ub.uni-leipzig.de>
Copyright: Universitätsbibliothek Leipzig, 2018
License: GPLv3
"""

import click

from .config import initialize, load_config
from .fetcher.mobygames import MobygamesFetcher
from .exporter import export_datasets
from .api import start_api

KNOWN_FETCH_SOURCES = ['mobygames', 'giantbomb']
KNOWN_UPDATE_SOURCES = ['giantbomb']

@click.group()
def cli():
    """
    daft -  video game metadata fetcher command line tool
    """

@cli.command()
@click.argument("source")
def fetch(source):
    """
    Fetch full dataset from source
    """
    if source not in KNOWN_FETCH_SOURCES:
        print("Source {} unknown.".format(source))
        exit(1)

    config = load_config()

    if source == "mobygames":
        mobygames = MobygamesFetcher(
            data_dir=config["project"]["data_dir"], 
            api_key=config["sources"]["mobygames"]["api_key"])
        mobygames.fetch()


@cli.command()
def init():
    """
    Initializes daft by creating a config.yml template.
    """
    initialize()


@cli.command()
def export():
    """
    Export standardized datasets.
    """
    export_datasets()


@cli.command()
def punk():
    """
    Daft Punk
    """
    print("5555")

@cli.command()
@click.option("--host", default="127.0.0.1", show_default=True)
@click.option("--port", default=6661, show_default=True)
@click.option("--debug/--no-debug", default=True)
def api(host, port, debug):
    start_api(host, port, debug)

if __name__ == "__main__":
    cli()
