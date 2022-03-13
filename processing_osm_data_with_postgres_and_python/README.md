# Processing OpenStreetMap Data with PostgreSQL and Python

This folder contains examples and files related to my PyConDE2022 talk.

## Requires

- osmium (^1.1.1)
- osm2pgsql (^1.6.0)

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
        tags->'de:place' = '"city"'
    AND
        tags->>'name'::text IN(
            'Berlin','Hamburg','München','Köln','Frankfurt am Main',
            'Stuttgart','Düsseldorf','Leipzig','Dortmund','Essen'
        )
) as dp
GROUP BY
    dp.name
```
