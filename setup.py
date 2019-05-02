from setuptools import setup
from os.path import abspath, dirname, join

base_path = dirname(abspath(__file__))

with open(join(base_path, "requirements.txt")) as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name="daft",
    version="0.1",
    packages=["daft", "daft.fetcher", "daft.reader"],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        daft=daft.tool:cli
    """
)
