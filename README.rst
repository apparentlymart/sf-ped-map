sf-ped-map
==========

OpenStreetMap-based San Francisco Map for Pedestrians.

This is an experiment in an alternative rendering of OpenStreetMap data to create a map that emphasizes features that
are interesting to pedestrians rather than those that are interesting to motorists.

`A preview snapshot of the rendering <http://a.tiles.mapbox.com/v3/apparentlymart.PedMap/page.html#17/37.78900/-122.39732>`_
is available on MapBox, which is a toolchain for creating and hosting maps.

The main features are:

* Footways are shown as green dotted lines, both when they are alongside roads and when they are independent.

* Roads that have no attached sidewalks are de-emphasized since they are useful to pedestrians only as landmarks.
  
* Roads that have public transit service are highlighted in orange, since these are in many ways the "trunk routes"
  of the pedestrian network. (though the OSM data for this is quite spotty in San Francisco at the time of writing.)
  
* Businesses and amenities such as shops, restaurants, schools and churches are prioritized over vehicle-only features
  such as parking lots.

Project Structure
-----------------

This project consists of three main parts:

* A Python script ``jenny.py`` that parses the OSM data snapshot and produces a number of CSV files describing the
  different interesting features.
  
* A `CartoCSS <https://www.mapbox.com/tilemill/docs/manual/carto/>`_ stylesheet (in ``style.mss``) to style those CSV
  layers.
  
* A `TileMill <https://www.mapbox.com/tilemill/>`_ project (in ``project.mml``) that specifies the various layers in
  the correct order to achieve the desired rendering.
  
If you wish to build your own map tiles from this project, the first step is to run the generation script to produce
the CSV files, and once that's done you should be able to load the project in TileMill to preview the map and
optionally render some static tiles to disk that can be rendered using the normal OSM tools.

If you want to produce a ped map for a different area of the world, you can export an OSM subset using
`the standard OSM tools <http://www.openstreetmap.org/export#map=16/40.7388/-73.9899>`_ and alter the generation
script to read that file instead. However, I put considerable work into adding sidewalk tagging to downtown
San Francisco before I was able to render the San Francisco map, and so it's possible that similar work will be
required in other areas before an accurate pedestrian map can be produced.

License
-------

This is an exploratory project and I encourage others to build on it to produce other alternative map renderings from
OSM data. The content in this repository is therefore all placed into the public domain, with the exception of the
OSM snapshot of San Francisco which is derived from OSM data and is thus under the same
`Open Data Commons Open Database License <http://opendatacommons.org/licenses/odbl/1.0/>`_.

I'm curious to see what others come up with, so please let me know if you have anything interesting to share.
