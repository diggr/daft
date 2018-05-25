from setuptools import setup

setup(
    name="daft",
    version="0.1",
    packages=["daft"],
    install_requires=[
        "Click", 
        "requests", 
        "pit", 
        "PyYAML"],
    entry_points="""
        [console_scripts]
        daft=daft_tool:daft_tool
    """
)