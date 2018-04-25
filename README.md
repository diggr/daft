# daft - data fetch tool

Fetch tool for video game meta data from various sources.
Writes fetched data into a zip archive.

Supported sources:
- Mobygames
- Giantbomb

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
```
