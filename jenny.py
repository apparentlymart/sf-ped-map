
import sqlite3
import xml.etree.ElementTree as ET
import csv
from shapely.geometry import Point, LineString, Polygon
from shapely.wkb import loads, dumps

tree = ET.parse("sfsubset.osm")
root = tree.getroot()

test_csv_f = open("layers/pointtest.csv", "wb")
test_csv = csv.writer(test_csv_f)

test_csv.writerow([ "name", "wkt" ])

nodes = {}
ways = {}
relations = {}


def tags_from_child_elems(elem):
    tags = {}
    for child_elem in elem:
        if child_elem.tag == "tag":
            tags[child_elem.attrib["k"]] = child_elem.attrib["v"]
    return tags


class Node(object):

    def __init__(self, osm_id, lon, lat, tags):
        self.id = osm_id
        self.lon = lon
        self.lat = lat
        self.tags = tags
        self.point = Point(lon, lat)

    @classmethod
    def from_xml_elem(cls, elem):
        osm_id = elem.attrib["id"]
        lat = float(elem.attrib["lat"])
        lon = float(elem.attrib["lon"])
        tags = tags_from_child_elems(elem)
        return cls(osm_id, lon, lat, tags)


class Way(object):

    def __init__(self, osm_id, nodes, tags):
        self.id = osm_id
        self.nodes = nodes
        self.tags = tags
        coords = [(n.lon, n.lat) for n in nodes]
        self.line_string = LineString(coords)
        if len(coords) > 3:
            self.polygon = Polygon(list(coords[:-1]))
        else:
            # Make a fake polygon just so there's always something
            # at self.polygon and we don't blow up when we encounter
            # malformed data. This will make a pretty dumb polygon, though.
            self.polygon = Polygon(coords * 3)

    @classmethod
    def from_xml_elem(cls, elem):
        osm_id = elem.attrib["id"]
        tags = tags_from_child_elems(elem)
        new_nodes = []
        for child_elem in elem:
            if child_elem.tag == "nd":
                node_id = child_elem.attrib["ref"]
                node = nodes[node_id]
                new_nodes.append(node)
        return cls(osm_id, new_nodes, tags)


class RelationMember(object):

    def __init__(self, obj, role):
        self.object = obj
        self.role = role

    @classmethod
    def from_xml_elem(cls, elem):
        member_type = elem.attrib["type"]
        ref = elem.attrib["ref"]
        role = elem.attrib["role"]
        if member_type == "way":
            obj = ways.get(ref, None)
        elif member_type == "node":
            obj = nodes.get(ref, None)
        elif member_type == "relation":
            # Our target relation might not have been loaded yet,
            # so we'll stash its id for now and fix it up later.
            obj = ref
        else:
            # Unknown target type
            obj = None

        return cls(obj, role)


class Relation(object):

    def __init__(self, osm_id, members, tags):
        self.id = osm_id
        self.members = members
        self.tags = tags

    @classmethod
    def from_xml_elem(cls, elem):
        osm_id = elem.attrib["id"]
        tags = tags_from_child_elems(elem)
        members = []
        for child_elem in elem:
            if child_elem.tag == "member":
                member = RelationMember.from_xml_elem(child_elem)
                if member is not None:
                    members.append(member)
        return cls(osm_id, members, tags)

    def members_by_type(self, member_type):
        return (m for m in self.members if type(m.object) is member_type)


class DataFile(object):

    def __init__(self, csv, tag_keys):
        self.csv = csv
        self.tag_keys = tag_keys
        self.csv.writerow(["wkt"] + [key.replace(":", "__") for key in tag_keys])

    @classmethod
    def open_new(cls, fn, tag_keys):
        full_name = "layers/%s.csv" % fn
        f = open(full_name, 'wb')
        csv_w = csv.writer(f)
        return cls(csv_w, tag_keys)

    def add_point(self, obj):
        wkt = obj.point.wkt
        others = [obj.tags.get(k, "").encode("utf-8") for k in self.tag_keys]
        self.csv.writerow([wkt] + others)

    def add_way(self, obj):
        wkt = obj.line_string.wkt
        others = [obj.tags.get(k, "").encode("utf-8") for k in self.tag_keys]
        self.csv.writerow([wkt] + others)

    def add_polygon(self, obj):
        wkt = obj.polygon.wkt
        others = [obj.tags.get(k, "").encode("utf-8") for k in self.tag_keys]
        self.csv.writerow([wkt] + others)


for elem in root:

    if elem.tag == "node":
        node = Node.from_xml_elem(elem)
        nodes[node.id] = node

        #point = node.point
        #name = node.tags.get("name", None)
        #if name is not None:
        #    print repr([name, point.wkt])
        #    test_csv.writerow([name.encode("utf-8"), point.wkt])

    elif elem.tag == "way":
        way = Way.from_xml_elem(elem)
        ways[way.id] = way

    elif elem.tag == "relation":
        relation = Relation.from_xml_elem(elem)
        relations[relation.id] = relation


# Because the relations are a graph we save just relation id strings as
# members during loading and need to now fix them up to be real relation
# object references.
for relation_id, relation in relations.iteritems():
    for member in relation.members:
        if type(member.object) is str:
            member.object = relations.get(member.object, None)


### HERE COMES THE PART WHERE WE ACTUALLY DO THE DATA MANIPULATION!

# First, we process the relations and add extra annotations to the
# members of them so that this data is visible to the renderer, because the
# renderer doesn't "see" relations, only nodes and ways.
for relation_id, relation in relations.iteritems():
    relation_type = relation.tags.get("type")

    if relation_type == "route":
        route_type = relation.tags.get("route")
        if route_type in ("bus", "tram", "light_rail"):
            for member in relation.members_by_type(Way):
                member.object.tags["on_bus_route"] = "yes"


# Now we can generate the geometry CSV files
highways = DataFile.open_new("highways", [
    "name",
    "highway",
    "sidewalk_left",
    "sidewalk_right",
    "on_bus_route",
    "interesting_to_peds",
])
landuse = DataFile.open_new("landuse", [
    "landuse",
])
buildings = DataFile.open_new("buildings", [
    "name",
    "building:levels",
    "shop",
])
pois = DataFile.open_new("pois", [
    "name",
    "amenity",
    "shop",
    "office",
    "food",
    "cuisine",
])

for way_id, way in ways.iteritems():
    if "highway" in way.tags:
        if way.tags.get("area", None) != "yes":

            # Just turn paths into footways for ease of common rendering
            if way.tags["highway"] == "path":
                way.tags["highway"] = "footway"

            sidewalk = way.tags.get("sidewalk", None)
            sidewalk_left = False
            sidewalk_right = False
            if sidewalk == "both":
                sidewalk_left = True
                sidewalk_right = True
            elif sidewalk == "left":
                sidewalk_left = True
            elif sidewalk == "right":
                sidewalk_right = True
            elif sidewalk in ("none", "separate"):
                pass
            else:
                if way.tags.get("highway") not in ("motorway", "cycleway", "motorway_link", "service"):
                    sidewalk_left = True
                    sidewalk_right = True

            way.tags["sidewalk_left"] = "yes" if sidewalk_left else "no"
            way.tags["sidewalk_right"] = "yes" if sidewalk_right else "no"

            interesting_to_peds = (sidewalk_left or sidewalk_right)
            way.tags["interesting_to_peds"] = "yes" if interesting_to_peds else "no"

            highways.add_way(way)

    # Turn some area stuff into landuse for rendering simplicity
    if way.tags.get("amenity") == "parking" and "landuse" not in way.tags:
        way.tags["landuse"] = "parking"
    if way.tags.get("leisure") == "park" and "landuse" not in way.tags:
        way.tags["landuse"] = "park"

    if "landuse" in way.tags:
        landuse.add_polygon(way)

    if "building" in way.tags:
        buildings.add_polygon(way)


for node_id, node in nodes.iteritems():
    if node.tags.get("amenity") in ("fuel","parking","bicycle_parking","telephone","taxi","car_sharing","bench"):
        continue
    for poi_key in ("amenity", "shop", "food", "cuisine"):
        if poi_key in node.tags:
            pois.add_point(node)
