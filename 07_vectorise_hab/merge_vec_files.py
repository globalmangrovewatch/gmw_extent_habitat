import rsgislib.vectorutils
import glob

vec_files = glob.glob("gmw_hab_vec_tiles/*.gpkg")

out_vec_file = "gmw_hab_msk_v26.gpkg"
out_vec_lyr = "gmw_hab_msk_v26"

rsgislib.vectorutils.merge_vector_files(
    vec_files,
    out_vec_file=out_vec_file,
    out_vec_lyr=out_vec_lyr,
    out_format = "GPKG",
    out_epsg = 4326,
)
