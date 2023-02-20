import os

import rsgislib
import rsgislib.imageutils

out_dir = "base_tiles"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

pxl_res = 0.0002  # i.e., about 20 m (22.2 m)

rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()

rsgislib.imageutils.create_img_for_each_vec_feat(
    vec_file="gmw_degree_tiles.geojson",
    vec_lyr="gmw_degree_tiles",
    file_name_col="tile_name",
    out_img_path=out_dir,
    out_img_ext="tif",
    out_img_pxl_val=0.0,
    out_img_n_bands=1,
    out_img_res=pxl_res,
    gdalformat="GTIFF",
    datatype=rsgislib.TYPE_8UINT,
    snap_to_grid=True,
)
