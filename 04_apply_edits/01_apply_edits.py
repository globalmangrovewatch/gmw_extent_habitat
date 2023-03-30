import os

import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.vectorattrs
import rsgislib.rastergis

rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()

out_dir = "gmw_hab_tiles"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

add_dir = "../03_rasterise_hab_edits/gmw_hab_adds"
rm_dir = "../03_rasterise_hab_edits/gmw_hab_rms"
old_hab_dir = "../../data/gmw_hab_v11_tiles"

gmw_hab_prev_version = "v11"
gmw_hab_edit_version = "v11_to_v12"
gmw_hab_new_version = "v12"

gmw_tiles_vec_file = "../01_gmw_tiles/gmw_degree_tiles.geojson"
gmw_tile_vec_lyr = "gmw_degree_tiles"

tiles = rsgislib.vectorattrs.read_vec_column(
    vec_file=gmw_tiles_vec_file, vec_lyr=gmw_tile_vec_lyr, att_column="tile_name"
)
tile_params = list()
for tile in tiles:
    hab_img = os.path.join(old_hab_dir, f"gmw_{tile}_hab_{gmw_hab_prev_version}.kea")
    add_img = os.path.join(add_dir, f"gmw_{tile}_add_hab_{gmw_hab_edit_version}.tif")
    rm_img = os.path.join(rm_dir, f"gmw_{tile}_rm_hab_{gmw_hab_edit_version}.tif")

    out_img = os.path.join(out_dir, f"gmw_{tile}_hab_{gmw_hab_new_version}.kea")
    if not os.path.exists(out_img):
        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn("hab", hab_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn("add", add_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn("rm", rm_img, 1))
        rsgislib.imagecalc.band_math(
            out_img, "add==1?1:rm==1?0:hab", "KEA", rsgislib.TYPE_8UINT, band_defns
        )
        rsgislib.rastergis.pop_rat_img_stats(clumps_img=out_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True)
