import os
import math

os.environ["USE_PYGEOS"] = "0"
import geopandas
import rsgislib.tools.utils

# Copernicus_DSM_10_S90_00_W135_00.tar

gmw_tiles_gdf = geopandas.read_file("../01_gmw_tiles/gmw_degree_tiles.geojson")

cop_dem_tiles = list()
for index, tile in gmw_tiles_gdf.iterrows():
    if tile["tile_name"] in ["N32E130", "N35E138"]:
        if tile["MinY"] < 0:
            abs_lat_int = rsgislib.tools.utils.zero_pad_num_str(
                math.fabs(tile["MinY"]), str_len=2, integerise=True
            )
            lat_str = f"S{abs_lat_int}"
        else:
            abs_lat_int = rsgislib.tools.utils.zero_pad_num_str(
                math.fabs(tile["MinY"]), str_len=2, integerise=True
            )
            lat_str = f"N{abs_lat_int}"

        if tile["MinX"] < 0:
            abs_lon_int = rsgislib.tools.utils.zero_pad_num_str(
                math.fabs(tile["MinX"]), str_len=3, integerise=True
            )
            lon_str = f"W{abs_lon_int}"
        else:
            abs_lon_int = rsgislib.tools.utils.zero_pad_num_str(
                math.fabs(tile["MinX"]), str_len=3, integerise=True
            )
            lon_str = f"E{abs_lon_int}"

        cop_dem_file = f"Copernicus_DSM_10_{lat_str}_00_{lon_str}_00.tar"
        # print(cop_dem_file)
        cop_dem_tiles.append(cop_dem_file)

rsgislib.tools.utils.write_list_to_file(cop_dem_tiles, "cop_30_dem_gmw_tiles.txt")
