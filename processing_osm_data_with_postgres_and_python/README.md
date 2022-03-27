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
    --style=flex-config/amenities-and-boundaries.lua \
    --output flex
```

#### Now we are ready for analysis!

#### 4.

What are some tables we might want to create?

- amenity
- leisure
- building
- roads
- boundary


## osmium examples

## osm2pgsql lua import scripts

### Trash can query

```sql
WITH count_data as (
	SELECT
		pl.name as city
		, pl.geom
		, pp.osm_subtype as amenity
		, ST_Area(ST_Transform(pl.geom, 4326)::geography) / 1000000 as area_sq_km
		, pp.osm_subtype as amenity_type
		, count(*) as count
	FROM
		poi_point pp
	JOIN
		place_polygon pl
	ON
		ST_Contains(pl.geom, pp.geom)
	WHERE
	(
		pp.osm_type = 'amenity'
	AND
		pp.osm_subtype = 'waste_basket'
	)
	AND
		pl.name in (
			'Berlin','Hamburg','München','Köln','Frankfurt am Main',
			'Stuttgart','Düsseldorf','Leipzig','Dortmund','Essen'
		)
	AND
		round(ST_Area(ST_Transform(pl.geom, 4326)::geography) / 1000) / 1000 > 1
	GROUP BY
		pp.osm_subtype, pl.name, pl.geom
)

SELECT 
	city
	, amenity
	, area_sq_km
	, count
	, count / round(area_sq_km) as amenity_per_sq_km
FROM 
	count_data
ORDER BY
	5 desc;
```