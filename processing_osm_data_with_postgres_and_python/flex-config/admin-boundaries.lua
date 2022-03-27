local tables = {}

tables.admin_boundaries = osm2pgsql.define_way_table('admin_boundaries', {
    { column = 'level', type = 'integer' },
    { column = 'osm_type', type = 'text' },
    { column = 'tags', type = 'jsonb' },
    { column = 'geom', type = 'geometry', projection = 3857 },
})

function osm2pgsql.process_way(object)
    if object.tags.admin_level then
        local type = object:grab_tag('boundary')
        local level = object:grab_tag('admin_level')

        tables.admin_boundaries:add_row({
          osm_type = 'way',
          type = type,
          level = level,
          tags = object.tags,
          geom = { create = 'area' }
        })
    end
end

function osm2pgsql.process_relation(object)
    if object.tags.admin_level then
        local type = object:grab_tag('boundary')
        local level = object:grab_tag('admin_level')

        tables.admin_boundaries:add_row({
            osm_type = 'relation',
            type = type,
            level = level,
            tags = object.tags,
            geom = { create = 'area' }
        })
    end
end