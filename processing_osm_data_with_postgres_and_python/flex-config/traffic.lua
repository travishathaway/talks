---
--- Borrowed from the great project: https://github.com/rustprooflabs/pgosm-flex
--- (check it out for more examples!)
---

require "flex-config.helpers"

local tables = {}


tables.traffic_point = osm2pgsql.define_table({
    name = 'traffic_point',
    schema = schema_name,
    ids = { type = 'node', id_column = 'osm_id' },
    columns = {
        { column = 'osm_type',     type = 'text', not_null = true },
        { column = 'osm_subtype',     type = 'text' },
        { column = 'geom',     type = 'point' , projection = srid},
    }
})


tables.traffic_line = osm2pgsql.define_table({
    name = 'traffic_line',
    schema = schema_name,
    ids = { type = 'way', id_column = 'osm_id' },
    columns = {
        { column = 'osm_type',     type = 'text', not_null = true },
        { column = 'osm_subtype',     type = 'text' },
        { column = 'geom',     type = 'linestring' , projection = srid},
    }
})


tables.traffic_polygon = osm2pgsql.define_table({
    name = 'traffic_polygon',
    schema = schema_name,
    ids = { type = 'way', id_column = 'osm_id' },
    columns = {
        { column = 'osm_type',     type = 'text', not_null = true },
        { column = 'osm_subtype',     type = 'text' },
        { column = 'geom',     type = 'multipolygon' , projection = srid},
    }
})


-- Change function name here
function traffic_process_node(object)
    if not object.tags.highway and not object.tags.railway and not
            object.tags.barrier and not object.tags.traffic_calming and not
            object.tags.amenity and not object.tags.noexit
            then
        return
    end

    if object.tags.highway == 'traffic_signals'
            or object.tags.highway == 'mini_roundabout'
            or object.tags.highway == 'stop'
            or object.tags.highway == 'crossing'
            or object.tags.highway == 'speed_camera'
            or object.tags.highway == 'motorway_junction'
            or object.tags.highway == 'turning_circle'
            or object.tags.highway == 'ford'
            or object.tags.highway == 'street_lamp'
            or object.tags.highway == 'services'
            then
        local osm_type = object:grab_tag('highway')

        tables.traffic_point:add_row({
            osm_type = osm_type,
            geom = { create = 'point' }
        })

    elseif object.tags.railway == 'level_crossing' then
        local osm_type = 'crossing'

        tables.traffic_point:add_row({
            osm_type = osm_type,
            geom = { create = 'point' }
        })

    -- Beginning of traffic w/ subtypes
    elseif object.tags.barrier then
        local osm_type = 'barrier'
        local osm_subtype = object:grab_tag('barrier')

        tables.traffic_point:add_row({
            osm_type = osm_type,
            osm_subtype = osm_subtype,
            geom = { create = 'point' }
        })

    elseif object.tags.traffic_calming then
        local osm_type = 'traffic_calming'
        local osm_subtype = object:grab_tag('traffic_calming')

        tables.traffic_point:add_row({
            osm_type = osm_type,
            osm_subtype = osm_subtype,
            geom = { create = 'point' }
        })

    elseif object.tags.amenity == 'fuel'
            or object.tags.amenity == 'parking'
            or object.tags.amenity == 'bicycle_parking'
            then
        local osm_type = 'amenity'
        local osm_subtype = object:grab_tag('amenity')
        tables.traffic_point:add_row({
            osm_type = osm_type,
            osm_subtype = osm_subtype,
            geom = { create = 'point' }
        })


    elseif object.tags.noexit
            then
        local osm_type = 'noexit'
        -- No meaningful subtype, only defined value is "yes"
        -- https://wiki.openstreetmap.org/wiki/Key:noexit
        tables.traffic_point:add_row({
            osm_type = osm_type,
            geom = { create = 'point' }
        })

    else
        return
    end

end


-- Change function name here
function traffic_process_way(object)
    if not object.tags.highway and not object.tags.railway and not
            object.tags.barrier and not object.tags.traffic_calming and not
            object.tags.amenity  and not object.tags.noexit
            then
        return
    end

    if object.tags.highway == 'traffic_signals'
            or object.tags.highway == 'mini_roundabout'
            or object.tags.highway == 'stop'
            or object.tags.highway == 'crossing'
            or object.tags.highway == 'speed_camera'
            or object.tags.highway == 'motorway_junction'
            or object.tags.highway == 'turning_circle'
            or object.tags.highway == 'ford'
            or object.tags.highway == 'street_lamp'
            or object.tags.highway == 'services'
            then
        local osm_type = object:grab_tag('highway')

        if object.is_closed then
            tables.traffic_polygon:add_row({
                osm_type = osm_type,
                geom = { create = 'area' }
            })
        else
            tables.traffic_line:add_row({
                osm_type = osm_type,
                geom = { create = 'line' }
            })
        end

    elseif object.tags.railway == 'level_crossing' then
        local osm_type = 'crossing'

        if object.is_closed then
            tables.traffic_polygon:add_row({
                osm_type = osm_type,
                geom = { create = 'area' }
            })
        else
            tables.traffic_line:add_row({
                osm_type = osm_type,
                geom = { create = 'line' }
            })
        end

    -- Beginning of traffic w/ subtypes
    elseif object.tags.barrier then        
        local osm_type = 'barrier'
        local osm_subtype = object:grab_tag('barrier')

        if object.is_closed then
            tables.traffic_polygon:add_row({
                osm_type = osm_type,
                osm_subtype = osm_subtype,
                geom = { create = 'area' }
            })
        else
            tables.traffic_line:add_row({
                osm_type = osm_type,
                osm_subtype = osm_subtype,
                geom = { create = 'line' }
            })
        end

    elseif object.tags.traffic_calming then
        local osm_type = 'traffic_calming'
        local osm_subtype = object:grab_tag('traffic_calming')

        if object.is_closed then
            tables.traffic_polygon:add_row({
                osm_type = osm_type,
                osm_subtype = osm_subtype,
                geom = { create = 'area' }
            })
        else
            tables.traffic_line:add_row({
                osm_type = osm_type,
                osm_subtype = osm_subtype,
                geom = { create = 'line' }
            })
        end

    elseif object.tags.amenity == 'fuel'
            or object.tags.amenity == 'parking'
            or object.tags.amenity == 'bicycle_parking'
            then
        local osm_type = 'amenity'
        local osm_subtype = object:grab_tag('amenity')

        if object.is_closed then
            tables.traffic_polygon:add_row({
                osm_type = osm_type,
                osm_subtype = osm_subtype,
                geom = { create = 'area' }
            })
        else
            tables.traffic_line:add_row({
                osm_type = osm_type,
                osm_subtype = osm_subtype,
                geom = { create = 'line' }
            })
        end


    elseif object.tags.noexit
            then
        local osm_type = 'noexit'
        -- No meaningful subtype, only defined value is "yes"
        -- https://wiki.openstreetmap.org/wiki/Key:noexit

        if object.is_closed then
            -- noexit does not make sense for polygons
            return
        else
            tables.traffic_line:add_row({
                osm_type = osm_type,
                geom = { create = 'line' }
            })
        end

    else
        return
    end

    
end



if osm2pgsql.process_node == nil then
    -- Change function name here
    osm2pgsql.process_node = traffic_process_node
else
    local nested = osm2pgsql.process_node
    osm2pgsql.process_node = function(object)
        local object_copy = deep_copy(object)
        nested(object)
        -- Change function name here
        traffic_process_node(object_copy)
    end
end


if osm2pgsql.process_way == nil then
    -- Change function name here
    osm2pgsql.process_way = traffic_process_way
else
    local nested = osm2pgsql.process_way
    osm2pgsql.process_way = function(object)
        local object_copy = deep_copy(object)
        nested(object)
        -- Change function name here
        traffic_process_way(object_copy)
    end
end
