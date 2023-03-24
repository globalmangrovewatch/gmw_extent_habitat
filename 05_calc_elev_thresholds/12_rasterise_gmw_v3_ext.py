import glob
import os
import rsgislib.vectorutils.createrasters
import rsgislib.tools.filetools

base_imgs = glob.glob("../01_gmw_tiles/base_tiles/*.tif")
gmw_v3_ext_dir = (
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_v3_ext"
)
if not os.path.exists(gmw_v3_ext_dir):
    os.mkdir(gmw_v3_ext_dir)

gmw_vec_file = "/bigdata/petebunting/Dropbox/University/Research/Data/Mangroves/GMW/gmw_v3_fnl_mjr_v314.gpkg"
gmw_vec_lyr = "mng_mjr_2015"

for base_img in base_imgs:
    gmw_tile_basename = rsgislib.tools.filetools.get_file_basename(base_img)

    gmw_ext_img = os.path.join(gmw_v3_ext_dir, f"{gmw_tile_basename}_v3_2015_ext.kea")
    if not os.path.exists(gmw_ext_img):
        rsgislib.vectorutils.createrasters.rasterise_vec_lyr(
            gmw_vec_file,
            gmw_vec_lyr,
            input_img=base_img,
            output_img=gmw_ext_img,
            gdalformat="KEA",
            burn_val=1,
            datatype=rsgislib.TYPE_8UINT,
            att_column=None,
            use_vec_extent=False,
            thematic=True,
            no_data_val=0,
        )
