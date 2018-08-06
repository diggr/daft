from setuptools import setup

setup(
    name="daft",
    version="0.1",
    packages=["daft", "daft.fetcher", "daft.reader"],
    install_requires=[
        "SPARQLWrapper",
        "Click", 
        "requests", 
        "provit", 
        "pandas",
        "PyYAML"],
    entry_points="""
        [console_scripts]
        daft=daft.tool:cli
    """
)
