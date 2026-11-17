#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
# Supply a Geofabrik Taiwan PBF as first argument, or reuse the retained filtered PBF.
if [ "$#" -gt 0 ]; then
 osmium tags-filter "$1" w/highway=motorway,trunk,primary,secondary,motorway_link,trunk_link,primary_link,secondary_link -o source/roads.osm.pbf --overwrite
fi
osmium export source/roads.osm.pbf -o source/roads.geojson --overwrite
python3 scripts/build_roads.py
