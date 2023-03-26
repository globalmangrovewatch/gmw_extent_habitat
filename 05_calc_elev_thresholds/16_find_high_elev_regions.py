from typing import List, Dict
import glob
import os
import numpy
import tqdm
import rsgislib.tools.filetools
import rsgislib.imagecalc
import rsgislib.rastergis
import rsgislib.tools.utils
import rsgislib.vectorutils.createvectors

tile_max_elev_lut = rsgislib.tools.utils.read_json_to_dict("gmw_elev_tile_stats.json")

gmw_dems_dir = (
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_cop30_dem"
)
gmw_v3_ext_dir = (
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_v3_ext"
)

out_dir = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_v3_ext_high_elev"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

gmw_tile_elev_stats = dict()
for gmw_tile in tqdm.tqdm(tile_max_elev_lut):
    if tile_max_elev_lut[gmw_tile] > 50:
        gmw_ext_img = os.path.join(gmw_v3_ext_dir, f"{gmw_tile}_v3_2015_ext.kea")
        dem_img = os.path.join(gmw_dems_dir, f"{gmw_tile}_dem.kea")

        out_img = os.path.join(out_dir, f"{gmw_tile}_v3_2015_ext_elev_gt50.kea")
        if (
            os.path.exists(gmw_ext_img)
            and os.path.exists(dem_img)
            and (not os.path.exists(out_img))
        ):
            band_defns = list()
            band_defns.append(rsgislib.imagecalc.BandDefn("gmw", gmw_ext_img, 1))
            band_defns.append(rsgislib.imagecalc.BandDefn("dem", dem_img, 1))
            rsgislib.imagecalc.band_math(
                out_img,
                "(gmw==1)&&(dem>50)?1:0",
                "KEA",
                rsgislib.TYPE_8UINT,
                band_defns,
            )
            rsgislib.rastergis.pop_rat_img_stats(
                clumps_img=out_img,
                add_clr_tab=True,
                calc_pyramids=True,
                ignore_zero=True,
            )

        out_vec_lyr = f"{gmw_tile}_v3_2015_ext_elev_gt50"
        out_vec_file = os.path.join(out_dir, f"{out_vec_lyr}.gpkg")
        if os.path.exists(out_img) and (not os.path.exists(out_vec_file)):
            rsgislib.vectorutils.createvectors.polygonise_raster_to_vec_lyr(
                out_vec_file,
                out_vec_lyr,
                out_format="GPKG",
                input_img=out_img,
                img_band=1,
                mask_img=out_img,
                mask_band=1,
                replace_file=True,
                replace_lyr=True,
                pxl_val_fieldname="PXLVAL",
                use_8_conn=False,
            )
