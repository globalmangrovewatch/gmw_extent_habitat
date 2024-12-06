import rsgislib.vectorutils
import glob

vec_files = glob.glob("/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_v4021_mis_hab_tiles_vec/*.gpkg")

out_vec_file = "gmw_v4021_hab_msk_mis.gpkg"
out_vec_lyr = "gmw_v4021_hab_msk_mis"

rsgislib.vectorutils.merge_vector_files(
    vec_files,
    out_vec_file=out_vec_file,
    out_vec_lyr=out_vec_lyr,
    out_format = "GPKG",
    out_epsg = 4326,
)
