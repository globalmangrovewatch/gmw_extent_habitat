import numpy
import rsgislib.tools.utils
import geopandas

tile_max_elev_lut = rsgislib.tools.utils.read_json_to_dict("gmw_v3_v4_inter_elev_tile_stats.json")
gmw_prjs_lut = rsgislib.tools.utils.read_json_to_dict("../99_gmw_prj_definition/gmw_tile_prj_lut.json")

gmw_tiles_gdf = geopandas.read_file("gmw_v3_v4_inter_tiles_elev_prjs.geojson")

gmw_prj_l1_elevs = dict()
gmw_prj_l2_elevs = dict()
for gmw_tile in tile_max_elev_lut:
    #print(f"{gmw_tile}: {gmw_prjs_lut[gmw_tile]} = {tile_max_elev_lut[gmw_tile]}")

    gmw_prj = gmw_prjs_lut[gmw_tile]
    gmw_prj_l1 = int(gmw_prj.split("-")[1])

    gmw_tile_df = gmw_tiles_gdf[gmw_tiles_gdf["tile_name"] == gmw_tile]
    edit_elev_val = gmw_tile_df["edit_max_mng_elev"].values[0]
    if not numpy.isnan(edit_elev_val):
        tile_max_elev_lut[gmw_tile] = float(edit_elev_val)
        print(tile_max_elev_lut[gmw_tile])

    if tile_max_elev_lut[gmw_tile] > 0:
        if gmw_prj_l1 not in gmw_prj_l1_elevs:
            gmw_prj_l1_elevs[gmw_prj_l1] = tile_max_elev_lut[gmw_tile]
        else:
            if tile_max_elev_lut[gmw_tile] > gmw_prj_l1_elevs[gmw_prj_l1]:
                gmw_prj_l1_elevs[gmw_prj_l1] = tile_max_elev_lut[gmw_tile]

        if gmw_prj not in gmw_prj_l2_elevs:
            gmw_prj_l2_elevs[gmw_prj] = tile_max_elev_lut[gmw_tile]
        else:
            if tile_max_elev_lut[gmw_tile] > gmw_prj_l2_elevs[gmw_prj]:
                gmw_prj_l2_elevs[gmw_prj] = tile_max_elev_lut[gmw_tile]


#print(gmw_prj_l1_elevs)
#print(gmw_prj_l2_elevs)

for gmw_tile in tile_max_elev_lut:
    if tile_max_elev_lut[gmw_tile] < 5:
        gmw_prj = gmw_prjs_lut[gmw_tile]
        gmw_prj_l1 = int(gmw_prj.split("-")[1])
        if gmw_prj in gmw_prj_l2_elevs:
            tile_max_elev_lut[gmw_tile] = gmw_prj_l2_elevs[gmw_prj]
        elif gmw_prj_l1 in gmw_prj_l1_elevs:
            tile_max_elev_lut[gmw_tile] = gmw_prj_l1_elevs[gmw_prj_l1]
        else:
            tile_max_elev_lut[gmw_tile] = 35

rsgislib.tools.utils.write_dict_to_json(tile_max_elev_lut, "gmw_v3_v4_inter_elev_tile_base_thresholds.json")

for gmw_tile in tile_max_elev_lut:
    tile_max_elev_lut[gmw_tile] = tile_max_elev_lut[gmw_tile] * 1.2

rsgislib.tools.utils.write_dict_to_json(tile_max_elev_lut, "gmw_v3_v4_inter_elev_tile_fnl_thresholds.json")