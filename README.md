# daft - data fetch tool

![Python 3]( https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)

Fetch tool for video game meta data from various sources.
Writes fetched data into a zip archive.

![daft logo](assets/daft_header.png?raw=true "daft")

Supported sources:
- [Mobygames](https://mobygames.com)
- [Mediaart DB](https://mediaarts-db.bunka.go.jp/gm)
- [GameFAQs](https://gamefaqs.gamespot.com)

## Installation

This application provides a setup.py which helps installing this application.
To install run:

```bash
pip install -e .
```

## Usage

```bash
# create config.yml
daft --init

# fetch full dataset
daft SOURCE --fetch

# update dataset (if available)
daft SOURCE --update

# export standardized dataset
daft --export

# start daft api
daft api

```

## config file

The config.yml need to be in the project root directory and looks like this:

```yaml

project:
  name: "test"
  data_dir: "../../game_metadata/sources"
  export_dir: "../../game_metadata/daft_export"

sources:
  mobygames:
    api_key: "<YOUR_API_KEY_HERE>"

api:
  - mobygames

export:
  mobygames:
      - title
      - alt_titles
      - platforms
  mediaartdb:
      - title
      - alt_titles
      - platforms
```

* data_dir: directory for the raw source datafiles (e.g. generated via the fetch command)
* export_dir: directory for the stadardized dataset exort
* sources: configuration for the fetchers (api-keys etc.)
* export: configuration for the standardized dataset export (fields must be spezified in the respective dataset reader classes)
* api: list of datasets available through the api

## Reader classes

daft provides reader classes for all supported datasets. Theses reader classes provide a standardized interface.
A factory method is also provided.

Example:

```python
from daft.reader import get_dataset

# load mobygames dataset
mobygames = get_dataset("path_to_daft_directory", "mobygames")

# iterate through mobygames dataset
for game in mobygames:
    print(game["title"])
    break

# get specific mobygames entry via id 
game = mobygames["1564"]
print(game["title"])
```

The reader class returns game entries in the dataset with the following information:
* "id"
* "title"
* "alt_titles"
* "platforms": standardized platform names
* "raw": the complete dataset as a json dict

