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
from .fetcher.giantbomb import GiantbombFetcher
from .exporter import export_datasets

KNOWN_FETCH_SOURCES = ['mobygames', 'giantbomb']
KNOWN_UPDATE_SOURCES = ['giantbomb']

@click.group()
def cli():
    """
    daft -  video game metadata fetcher command line tool
    """


@cli.command()
@click.argument("source")
def update(source):
    """
    Fetch update from data source (if available)
    """
    if source not in KNOWN_UPDATE_SOURCES:
        print("Source {} unknown.".format(source))
        exit(1)

    if source == "giantbomb":
        giantbomb = GiantbombFetcher(data_dir=config["data_dir"], api_key=datasets["giantbomb"]["api_key"])
        giantbomb.fetch()
        giantbomb.update()


@cli.command()
@click.argument("source")
def fetch(source):
    """
    Fetch full dataset from source
    """
    if source not in KNOWN_FETCH_SOURCES:
        print("Source {} unknown.".format(source))
        exit(1)

    config, datasets = load_config()

    if source == "mobygames":
        mobygames = MobygamesFetcher(data_dir=config["data_dir"], api_key=datasets["mobygames"]["api_key"])
        mobygames.fetch()
    elif source == "giantbomb":
        giantbomb = GiantbombFetcher(data_dir=config["data_dir"], api_key=datasets["giantbomb"]["api_key"])
        giantbomb.fetch()

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


if __name__ == "__main__":
    cli()
