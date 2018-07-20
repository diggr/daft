# daft - data fetch tool

Fetch tool for video game meta data from various sources.
Writes fetched data into a zip archive.

Supported sources:
- Mobygames
- Giantbomb
- Mediaart DB

## installation

```
pip install -e .
```

## usage

```
# create config.yml
daft --init

# fetch full dataset
daft <source> --fetch

# update dataset (if available)
daft <source> --update

# export standardized dataset
daft --exoport
```

## config file

The config.yml need to be in the project root directory and looks like this:

```

project:
  name: "test"
  data_directory: "/home/pmuehleder/data/game_metadata/sources"
  export_directory: "/home/pmuehleder/data/game_metadata/daft_export"

datasets:
  mobygames:
    api_key: "***REMOVED***"
  giantbomb:
    api_key: "***REMOVED***"

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

* data_directory: directory for the raw source datafiles (e.g. generated via the fetch command)
* export_direcotry: directory for the stadardized dataset exort
* datasets: configuration for the fetchers (api-keys etc.)
* export: configuration for the standardized dataset export (fields must be spezified in the respective dataset reader classes)

## Reader classes

daft provides reader classes for all supported datasets. Theses reader classes provide a standardized interface.
A factory method is also provided.

Example:

```
from daft.reader import get_dataset

# load mobygames dataset
mobygames = get_dataset("path_to_daft_directory", "mobygames")

# iterate through mobygames dataset
for game in mobygames:
    print(game["title])
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

