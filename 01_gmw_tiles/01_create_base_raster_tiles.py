import os

import rsgislib
import rsgislib.imageutils

from osgeo import gdal

def create_img_for_each_vec_feat(
    vec_file: str,
    vec_lyr: str,
    file_name_col: str,
    out_img_path: str,
    out_img_ext: str,
    out_img_pxl_val: float,
    out_img_n_bands: int,
    out_img_res: float,
    gdalformat: str,
    datatype: int,
    snap_to_grid: bool = False,
    ignore_exist: bool = True,
):
    """
    A function to create a set of image files representing the extent of each
    feature in the inputted vector file.

    :param vec_file: the input vector file.
    :param vec_lyr: the input vector layer
    :param file_name_col: the name of the column in the vector layer which will be
                          used as the file names.
    :param out_img_path: output file path (directory) where the images will be saved.
    :param out_img_ext: the file extension to be added on to the output file names.
    :param out_img_pxl_val: output image pixel value
    :param out_img_n_bands: the number of image bands in the output image
    :param out_img_res: output image resolution, square pixels so a single value
    :param gdalformat: output image file format.
    :param datatype: is a rsgislib.TYPE_* value providing the data type of the
                     output image.
    :param snap_to_grid: snap the output image to a grid of whole numbers
                         with respect to the image pixel resolution.
    :param ignore_exist: ignore outputs which already exist and therefore
                         only create those which don't exist.
    """

    dsVecFile = gdal.OpenEx(vec_file, gdal.OF_VECTOR)
    if dsVecFile is None:
        raise rsgislib.RSGISPyException("Could not open '" + vec_file + "'")

    lyrVecObj = dsVecFile.GetLayerByName(vec_lyr)
    if lyrVecObj is None:
        raise rsgislib.RSGISPyException("Could not find layer '" + vec_lyr + "'")

    lyrSpatRef = lyrVecObj.GetSpatialRef()
    if lyrSpatRef is not None:
        wktstr = lyrSpatRef.ExportToWkt()
    else:
        wktstr = ""

    colExists = False
    feat_idx = 0
    lyrDefn = lyrVecObj.GetLayerDefn()
    for i in range(lyrDefn.GetFieldCount()):
        if lyrDefn.GetFieldDefn(i).GetName().lower() == file_name_col.lower():
            feat_idx = i
            colExists = True
            break

    if not colExists:
        dsVecFile = None
        raise rsgislib.RSGISPyException(
            "The specified column does not exist in the input layer; "
            "check case as some drivers are case sensitive."
        )

    lyrVecObj.ResetReading()
    for feat in lyrVecObj:
        geom = feat.GetGeometryRef()
        if geom is not None:
            env = geom.GetEnvelope()
            tilebasename = feat.GetFieldAsString(feat_idx)
            output_img = os.path.join(
                out_img_path, "{0}.{1}".format(tilebasename, out_img_ext)
            )
            create_out_file = True
            if ignore_exist and os.path.exists(output_img):
                create_out_file = False

            if create_out_file:
                print(output_img)
                rsgislib.imageutils.create_blank_img_from_bbox(
                    env,
                    wktstr,
                    output_img,
                    out_img_res,
                    out_img_pxl_val,
                    out_img_n_bands,
                    gdalformat,
                    datatype,
                    snap_to_grid,
                )

out_dir = "base_tiles"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

pxl_res = 0.0002  # i.e., about 20 m (22.2 m)

rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()

create_img_for_each_vec_feat(
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
    ignore_exist=True,
)
