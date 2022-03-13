local tables = {}

tables.amenities = osm2pgsql.define_way_table('amenity_polygons', {
    { column = 'type', type = 'text' },
    { column = 'osm_type', type = 'text' },
    { column = 'tags', type = 'jsonb' },
    { column = 'geom', type = 'geometry', projection = 3857 },
})

tables.amenity_points = osm2pgsql.define_node_table('amenity_points', {
    { column = 'type', type = 'text' },
    { column = 'tags', type = 'jsonb' },
    { column = 'geom', type = 'geometry', projection = 3857 },
})

function osm2pgsql.process_node(object)
    if object.tags.amenity or object.tags.shop then
        tables.amenity_points:add_row({
          type = object.tags.amenity,
          tags = object.tags,
          geom = { create = 'point' }
        })
    end
end

function osm2pgsql.process_way(object)
    if object.tags.amenity or object.tags.shop then
        tables.amenities:add_row({
          osm_type = 'way',
          type = object.tags.amenity,
          tags = object.tags,
          geom = { create = 'area' }
        })
    end
end

function osm2pgsql.process_relation(object)
    if object.tags.amenity or object.tags.shop then
        tables.amenities:add_row({
          osm_type = 'relation',
          type = object.tags.amenity,
          tags = object.tags,
          geom = { create = 'area' }
        })
    end
end