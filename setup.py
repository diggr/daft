from setuptools import setup
from os.path import abspath, dirname, join

setup(
    name="daft",
    version="1.0.0",
    packages=["daft", "daft.fetcher", "daft.reader"],
    entry_points="""
        [console_scripts]
        daft=daft.tool:cli
    """
)
