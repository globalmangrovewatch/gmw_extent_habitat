import glob

import rsgislib.vectorutils

vec_tiles = glob.glob("gmw_hab_vec_tiles/*.gpkg")

out_vec_file = "gmw_hab_msk_v15.gpkg"
out_vec_lyr = "gmw_hab_msk_v15"

rsgislib.vectorutils.merge_vector_files(
    vec_tiles, out_vec_file, out_vec_lyr, out_format="GPKG", out_epsg=4326
)
