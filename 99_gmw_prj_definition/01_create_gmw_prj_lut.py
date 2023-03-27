import os
os.environ['USE_PYGEOS'] = '0'

import geopandas
import rsgislib.tools.utils

gmw_tiles_gdf = geopandas.read_file("gmw_tiles_prj_def.geojson")

gmw_lvl1_prj_lst = list()
gmw_lvl2_prj_lst = list()

prjs_lut = dict()
tile_lut = dict()
for index, tile in gmw_tiles_gdf.iterrows():
    print(f"{tile['tile_name']} - {tile['gmw_prj']}")
    #tile["tile_name"]
    #tile["gmw_prj"]

    prj_name = tile["gmw_prj"]
    prj_name_parts = prj_name.split("-")
    gmw_lvl1_prj_lst.append(int(prj_name_parts[1]))
    gmw_lvl2_prj_lst.append(int(prj_name_parts[2]))

    tile_lut[tile["tile_name"]] = prj_name
    if prj_name not in prjs_lut:
        prjs_lut[prj_name] = list()
    prjs_lut[prj_name].append(tile["tile_name"])

rsgislib.tools.utils.write_dict_to_json(prjs_lut, "gmw_prj_lut.json")
rsgislib.tools.utils.write_dict_to_json(tile_lut, "gmw_tile_prj_lut.json")

