import glob
import os
import rsgislib.imageutils
import rsgislib.imageutils.imagelut
import rsgislib.tools.filetools

#base_imgs = glob.glob("../01_gmw_tiles/base_tiles/*.tif")

base_imgs = ["../01_gmw_tiles/base_tiles/N30E140.tif",
             "../01_gmw_tiles/base_tiles/N00W097.tif",
             "../01_gmw_tiles/base_tiles/N00W096.tif",
             "../01_gmw_tiles/base_tiles/N17E114.tif",
             "../01_gmw_tiles/base_tiles/S01W096.tif"]


gmw_dems_dir = (
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_cop30_dem"
)
if not os.path.exists(gmw_dems_dir):
    os.mkdir(gmw_dems_dir)

lut_vec_file = (
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_scns_lut.gpkg"
)
lut_vec_lyr = "cop30_scns_lut"

tmp_dir = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/tmp"

for base_img in base_imgs:
    gmw_tile_basename = rsgislib.tools.filetools.get_file_basename(base_img)
    out_dem_img = os.path.join(gmw_dems_dir, f"{gmw_tile_basename}_dem.kea")
    print(out_dem_img)
    if not os.path.exists(out_dem_img):
        scn_bbox = rsgislib.imageutils.get_img_bbox(base_img)
        dem_img = rsgislib.imageutils.imagelut.get_raster_lyr(
            scn_bbox, lut_db_file=lut_vec_file, lyr_name=lut_vec_lyr, tmp_dir=tmp_dir
        )
        print(dem_img)
        if dem_img is not None:
            rsgislib.imageutils.resample_img_to_match(
                in_ref_img=base_img,
                in_process_img=dem_img,
                output_img=out_dem_img,
                gdalformat="KEA",
                interp_method=rsgislib.INTERP_CUBICSPLINE,
                datatype=rsgislib.TYPE_32FLOAT,
                no_data_val=-32767,
                multicore=False,
            )
            rsgislib.imageutils.pop_img_stats(
                out_dem_img, use_no_data=True, no_data_val=-32767, calc_pyramids=True
            )


