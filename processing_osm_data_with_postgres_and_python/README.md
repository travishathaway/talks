# Processing OpenStreetMap Data with PostgreSQL and Python

This folder contains and example CLI program which was briefly described in the
PyConDE 2022 talk, "Processing OpenStreetMap Data with PostgreSQL and Python".

Check out the slides to that presentation here:
[Slides link](https://docs.google.com/presentation/d/1nFQr_NUr-QmG0n-wusnctjnAl8YUKmMuz3PhU_FoTYo/edit?usp=sharing)

## Getting started

This project is managed via poetry. To begin using run the following commands:

```bash
$ poetry install 
# ... Installs dependencies
$ poetry shell
# ... Activates virtual environment
```

## Other requirements

- osmium (^1.1.1)
- osm2pgsql (^1.6.0)

## osmprj CLI

Below are the commands for this CLI:

### `osmprj extract`

```
Usage: osm extract [OPTIONS] CONFIG OSM_DATA_FILE

  Extracts the given bounding boxes in CONFIG and combines them all into a
  single osm.pbf file

Options:
  -o, --output TEXT
  --silent
  --dry-run
  --help             Show this message and exit.
```

### `osmprj report`

```
Usage: osmprj report [OPTIONS] COMMAND [ARGS]...

  These sub-commands are responsible for generating reports

Options:
  --help  Show this message and exit.

Commands:
  amenity_city
  parking_space
```