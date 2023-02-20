import os

import rsgislib
import rsgislib.vectorattrs
import rsgislib.vectorutils.createrasters
import rsgislib.imageutils

rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()


def rasterise_vec_to_tile(params):
    vec_lyr_obj = params[0]
    base_img = params[1]
    out_img = params[2]
    rsgislib.imageutils.create_copy_img(
        base_img, out_img, 1, 0, "GTIFF", rsgislib.TYPE_8UINT
    )
    rsgislib.vectorutils.createrasters.rasterise_vec_lyr_obj(
        vec_lyr_obj,
        output_img=out_img,
        burn_val=1,
        att_column=None,
        thematic=False,
        no_data_val=0,
    )
    rsgislib.imageutils.pop_thmt_img_stats(
        out_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True
    )


base_tiles_dir = "../01_gmw_tiles/base_tiles"

out_add_dir = "gmw_hab_adds"
if not os.path.exists(out_add_dir):
    os.mkdir(out_add_dir)

out_rm_dir = "gmw_hab_rms"
if not os.path.exists(out_rm_dir):
    os.mkdir(out_rm_dir)

gmw_hab_add_vec_file = "00_edits/edits_v9_v10/habitat_additions_v9_to_v10.geojson"
gmw_hab_add_vec_lyr = "habitat_additions_v9_to_v10"

gmw_hab_rm_vec_file = "00_edits/edits_v9_v10/habitat_remove_v9_to_v10.geojson"
gmw_hab_rm_vec_lyr = "habitat_remove_v9_to_v10"

gmw_hab_version = "v9_to_v10"

add_vec_ds_obj, add_vec_lyr_obj = rsgislib.vectorutils.read_vec_lyr_to_mem(
    vec_file=gmw_hab_add_vec_file, vec_lyr=gmw_hab_add_vec_lyr
)

rm_vec_ds_obj, rm_vec_lyr_obj = rsgislib.vectorutils.read_vec_lyr_to_mem(
    vec_file=gmw_hab_rm_vec_file, vec_lyr=gmw_hab_rm_vec_lyr
)


gmw_tiles_vec_file = "../01_gmw_tiles/gmw_degree_tiles.geojson"
gmw_tile_vec_lyr = "gmw_degree_tiles"

tiles = rsgislib.vectorattrs.read_vec_column(
    vec_file=gmw_tiles_vec_file, vec_lyr=gmw_tile_vec_lyr, att_column="tile_name"
)
tile_params = list()
for tile in tiles:
    base_img = os.path.join(base_tiles_dir, f"{tile}.tif")
    out_add_img = os.path.join(out_add_dir, f"gmw_{tile}_add_hab_{gmw_hab_version}.tif")
    if not os.path.exists(out_add_img):
        rasterise_vec_to_tile([add_vec_lyr_obj, base_img, out_add_img])

    out_rm_img = os.path.join(out_rm_dir, f"gmw_{tile}_rm_hab_{gmw_hab_version}.tif")
    if not os.path.exists(out_rm_img):
        rasterise_vec_to_tile([rm_vec_lyr_obj, base_img, out_rm_img])

add_vec_ds_obj = None
rm_vec_ds_obj = None
