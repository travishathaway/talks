# Processing OpenStreetMap Data with PostgreSQL and Python

This folder contains examples and files related to my PyConDE2022 talk.

## Requires

- osmium (^1.1.1)
- osm2pgsql (^1.6.0)

## Problem scenario

You have just won a contract from *Trashcans United* a world renown trashcan advocacy group.

### Requirements:

- Statistics for all trash cans in the 10 largest cities in Germany
- Tracking the number of trash cans over time (ideally every year)
- Adaptability as they may wish to include more cities and countries over time.

### Steps to solving this problem

#### 1. Compile a list of the top ten cities in Germany by population

1. Berlin
2. Hamburg
3. München
4. Köln
5. Frankfurt am Main
6. Stuttgart
7. Düsseldorf
8. Leipzig
9. Dortmund
10. Essen

#### 2. Download applicable OSM data

```bash
curl -O https://download.geofabrik.de/europe/germany-latest.osm.pbf
```

#### 3. Extract admin boundaries and amenities from this data set

```bash
trash data import germany-latest.osm.pbf \
    --filters='/boundary=administrative /amenity /shop' \
    --database=germany_osm \
    --style=osm2pgsql_flex_scripts/amenities-and-boundaries.lua \
    --output flex
```

#### Now we are ready for analysis!

#### 4.


## osmium examples

## osm2pgsql lua import scripts

```sql

SELECT
    dp.name,
    min(ST_X((dp).bounding_box.geom)) as lon_min,
    min(ST_Y((dp).bounding_box.geom)) as lat_min,
    max(ST_X((dp).bounding_box.geom)) as lon_max,
    max(ST_Y((dp).bounding_box.geom)) as lat_max
FROM (
    SELECT
        tags->'name' as name,
        ST_DumpPoints(ST_Envelope(ST_Transform(geom, 4236))) as bounding_box
    FROM
        admin_boundaries
    WHERE
        tags->>'de:place' = 'city'
    AND
        tags->>'name'::text IN(
            'Berlin','Hamburg','München','Köln','Frankfurt am Main',
            'Stuttgart','Düsseldorf','Leipzig','Dortmund','Essen'
        )
) as dp
GROUP BY
    dp.name
```
