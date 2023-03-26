import os
os.environ['USE_PYGEOS'] = '0'

import rsgislib.tools.utils
import geopandas

tile_max_elev_lut = rsgislib.tools.utils.read_json_to_dict("gmw_elev_tile_stats.json")
gmw_prjs_lut = rsgislib.tools.utils.read_json_to_dict("../gmw_projects_luts.json")
gmw_tiles_prj_lut = dict()
for gmw_prj in gmw_prjs_lut:
    for gmw_tile in gmw_prjs_lut[gmw_prj]:
        gmw_tiles_prj_lut[gmw_tile] = gmw_prj

gmw_tiles_gdf = geopandas.read_file("../01_gmw_tiles/gmw_degree_tiles.geojson")

max_elev_lst = list()
gmw_prj_lst = list()
gmw_lvl1_prj_lst = list()
gmw_lvl2_prj_lst = list()

for index, tile in gmw_tiles_gdf.iterrows():
    print(tile["tile_name"])

    if tile["tile_name"] in tile_max_elev_lut:
        max_elev_lst.append(tile_max_elev_lut[tile["tile_name"]])
    else:
        max_elev_lst.append(-9999)

    if tile["tile_name"] in gmw_tiles_prj_lut:
        prj_name = gmw_tiles_prj_lut[tile["tile_name"]]
        prj_name_parts = prj_name.split("-")
        gmw_prj_lst.append(prj_name)
        gmw_lvl1_prj_lst.append(int(prj_name_parts[1]))
        gmw_lvl2_prj_lst.append(int(prj_name_parts[2]))
    else:
        gmw_prj_lst.append("")
        gmw_lvl1_prj_lst.append(0)
        gmw_lvl2_prj_lst.append(0)

gmw_tiles_gdf["max_mng_elev"] = max_elev_lst
gmw_tiles_gdf["gmw_prj"] = gmw_prj_lst
gmw_tiles_gdf["gmw_prj_lvl1"] = gmw_lvl1_prj_lst
gmw_tiles_gdf["gmw_prj_lvl2"] = gmw_lvl2_prj_lst

gmw_tiles_gdf.to_file("gmw_tiles_elev_prjs.geojson", driver="GeoJSON")

