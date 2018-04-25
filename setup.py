from setuptools import setup

setup(
    name="daft",
    version="0.1",
    py_modules=["fetcher"],
    install_requires=[
        "Click", 
        "requests", 
        "pit", 
        "PyYAML"],
    entry_points="""
        [console_scripts]
        daft=daft:daft_tool
    """
)