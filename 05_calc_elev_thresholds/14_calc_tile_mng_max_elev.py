from typing import List, Dict
import glob
import os
import numpy
import tqdm
import rsgislib.tools.filetools
import rsgislib.imageutils
import rsgislib.tools.utils

from osgeo import gdal

def calc_sum_stats_msk_vals(
    input_img:str, img_band:int, img_msk:str, msk_band:int, msk_vals:List[int]=None, use_no_data:bool=True, no_data_val:float=None, out_no_data_val:float=-9999,
):
    """
    A function which reads the image bands (values and mask) into memory
    calculate standard summary statistics (min, max, mean, std dev, median)

    :param input_img: image values image file path.
    :param img_band: values image band
    :param img_msk: file path for image mask.
    :param msk_band: mask image band
    :param msk_vals: a list of values within the mask can be provided to just consider
                    a limited number of mask values when calculating the histograms.
                    If None (default) then calculated for all mask values.
    :param use_no_data: Use no data value for the input image.
    :param no_data_val: no data value for the input image (if None then read from input image header)
    :param out_no_data_val: output no data value written to output dict if there are no valid pixel values.
    :return: returns a dict summary statistics (Min, Max, Mean, Std Dev, Median)

    """
    if use_no_data and (no_data_val is None):
        no_data_val = rsgislib.imageutils.get_img_no_data_value(input_img, img_band=img_band)

    img_vals_ds = gdal.Open(input_img)
    img_vals_band = img_vals_ds.GetRasterBand(img_band)
    vals_arr = img_vals_band.ReadAsArray()
    img_vals_ds = None

    img_msk_ds = gdal.Open(img_msk)
    img_msk_band = img_msk_ds.GetRasterBand(msk_band)
    msk_arr = img_msk_band.ReadAsArray()
    img_msk_ds = None

    if msk_vals is None:
        uniq_vals = numpy.unique(msk_arr)
        uniq_vals = uniq_vals[uniq_vals != 0]
    else:
        uniq_vals = msk_vals

    pxls_vals_lst = list()
    for msk_val in uniq_vals:
        pxls_vals_lst.append(vals_arr[msk_arr == msk_val])

    stats_dict = dict()
    stats_dict["min"] = out_no_data_val
    stats_dict["max"] = out_no_data_val
    stats_dict["mean"] = out_no_data_val
    stats_dict["stddev"] = out_no_data_val
    stats_dict["median"] = out_no_data_val

    pxls_vals = numpy.stack(pxls_vals_lst).flatten()
    if use_no_data:
        pxls_vals = pxls_vals[pxls_vals != no_data_val]

    if len(pxls_vals) > 0:
        stats_dict["min"] = pxls_vals.min()
        stats_dict["max"] = pxls_vals.max()
        stats_dict["mean"] = pxls_vals.mean()
        stats_dict["stddev"] = pxls_vals.std()
        stats_dict["median"] = numpy.median(pxls_vals)

    vals_arr = None
    msk_arr = None
    pxls_vals = None

    return stats_dict


base_imgs = glob.glob("../01_gmw_tiles/base_tiles/*.tif")
gmw_dems_dir = (
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_cop30_dem"
)
gmw_v3_ext_dir = (
    "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_v3_ext"
)

gmw_tile_elev_stats = dict()
for base_img in tqdm.tqdm(base_imgs):
    gmw_tile_basename = rsgislib.tools.filetools.get_file_basename(base_img)
    gmw_ext_img = os.path.join(gmw_v3_ext_dir, f"{gmw_tile_basename}_v3_2015_ext.kea")
    dem_img = os.path.join(gmw_dems_dir, f"{gmw_tile_basename}_dem.kea")

    if os.path.exists(gmw_ext_img) and os.path.exists(dem_img):
        dem_stats = calc_sum_stats_msk_vals(
            input_img=dem_img, img_band=1, img_msk=gmw_ext_img, msk_band=1, msk_vals=[1], use_no_data=True, no_data_val=None,
            out_no_data_val=-9999,
        )
        gmw_tile_elev_stats[gmw_tile_basename] = dem_stats['max']

    else:
        gmw_tile_elev_stats[gmw_tile_basename] = -9999


rsgislib.tools.utils.write_dict_to_json(gmw_tile_elev_stats, "gmw_elev_tile_stats.json")
