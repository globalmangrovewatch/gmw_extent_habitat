import glob
import rsgislib.vectorutils

vec_files = glob.glob(
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_v3_v4_002_inter_ext_high_elev/*.gpkg"
)

rsgislib.vectorutils.merge_vector_files(
    vec_files,
    out_vec_file="gmw_v3_v4_002_inter_high_elev_rgns.gpkg",
    out_vec_lyr="gmw_v3_v4_002_inter_high_elev_rgns",
    out_format="GPKG",
)
