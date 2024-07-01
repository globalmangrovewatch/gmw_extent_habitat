import os

import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.vectorattrs
import rsgislib.vectorutils.createvectors

rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()

out_dir = "gmw_hab_vec_tiles"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

hab_dir = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_hab_v19_tiles"
#hab_dir = "../04_apply_edits/gmw_hab_tiles"

gmw_hab_version = "v19"

gmw_tiles_vec_file = "../01_gmw_tiles/gmw_degree_tiles.geojson"
gmw_tile_vec_lyr = "gmw_degree_tiles"

tiles = rsgislib.vectorattrs.read_vec_column(
    vec_file=gmw_tiles_vec_file, vec_lyr=gmw_tile_vec_lyr, att_column="tile_name"
)
tile_params = list()
for tile in tiles:
    hab_img = os.path.join(hab_dir, f"gmw_{tile}_hab_{gmw_hab_version}.kea")
    if os.path.exists(hab_img):
        n_pxl_counts = rsgislib.imagecalc.count_pxls_of_val(hab_img, vals=[1], img_band=1)

        if n_pxl_counts[0] > 0:
            out_vec_lyr = f"gmw_{tile}_hab_{gmw_hab_version}"
            out_vec_file = os.path.join(out_dir, f"{out_vec_lyr}.gpkg")
            if not os.path.exists(out_vec_file):
                rsgislib.vectorutils.createvectors.polygonise_raster_to_vec_lyr(
                    out_vec_file,
                    out_vec_lyr,
                    out_format="GPKG",
                    input_img=hab_img,
                    img_band=1,
                    mask_img=hab_img,
                    mask_band=1,
                    replace_file=True,
                    replace_lyr=True,
                    pxl_val_fieldname="PXLVAL",
                    use_8_conn=False,
                )
