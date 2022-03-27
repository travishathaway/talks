---
--- Borrowed from the great project: https://github.com/rustprooflabs/pgosm-flex
--- (check it out for more examples!)
---

-- tags.lua
-- All OSM tag data in a single table w/out geometry
require "flex-config.helpers"


local tags_table = osm2pgsql.define_table{
    name = "tags",
    schema = schema_name,
    -- This will generate a column "osm_id INT8" for the id, and a column
    -- "geom_type CHAR(1)" for the type of object: N(ode), W(way), R(relation)
    ids = { type = 'any', id_column = 'osm_id', type_column = 'geom_type' },
    columns = {
        { column = 'tags',  type = 'jsonb' },
    }
}

-- Helper function to remove some of the tags we usually are not interested in.
-- Returns true if there are no tags left.
function clean_tags(tags)
    tags.odbl = nil
    tags.created_by = nil
    tags.source = nil
    tags['source:ref'] = nil

    return next(tags) == nil
end

function process(object)
    if clean_tags(object.tags) then
        return
    end
    tags_table:add_row({
        tags = object.tags
    })
end

function all_tags_process_node(object)
    process(object)
end

function all_tags_process_way(object)
    process(object)
end

function all_tags_process_relation(object)
    process(object)
end



if osm2pgsql.process_node == nil then
    -- Change function name here
    osm2pgsql.process_node = all_tags_process_node
else
    local nested = osm2pgsql.process_node
    osm2pgsql.process_node = function(object)
        local object_copy = deep_copy(object)
        nested(object)
        -- Change function name here
        all_tags_process_node(object_copy)
    end
end


if osm2pgsql.process_way == nil then
    -- Change function name here
    osm2pgsql.process_way = all_tags_process_way
else
    local nested = osm2pgsql.process_way
    osm2pgsql.process_way = function(object)
        local object_copy = deep_copy(object)
        nested(object)
        -- Change function name here
        all_tags_process_way(object_copy)
    end
end



if osm2pgsql.process_relation == nil then
    -- Change function name here
    osm2pgsql.process_relation = all_tags_process_relation
else
    local nested = osm2pgsql.process_relation
    osm2pgsql.process_relation = function(object)
        local object_copy = deep_copy(object)
        nested(object)
        -- Change function name here
        all_tags_process_relation(object_copy)
    end
end
