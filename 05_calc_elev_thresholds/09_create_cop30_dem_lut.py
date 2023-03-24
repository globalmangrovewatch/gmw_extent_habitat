import glob
import rsgislib.imageutils.imagelut

input_imgs = glob.glob(
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_extract_tiles/*/DEM/*.tif"
)

vec_file = (
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_scns_lut.gpkg"
)
vec_lyr = "cop30_scns_lut"

rsgislib.imageutils.imagelut.create_img_extent_lut(
    input_imgs,
    vec_file,
    vec_lyr,
    out_format="GPKG",
    ignore_none_imgs=False,
    out_proj_wgs84=False,
    overwrite_lut_file=True,
)
