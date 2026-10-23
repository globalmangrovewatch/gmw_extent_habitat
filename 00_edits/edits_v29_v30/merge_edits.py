import rsgislib.vectorutils

in_add_vec_file = "/Users/pfb/Library/CloudStorage/Dropbox/University/Research/Data/Mangroves/GMW_Habitat_Layers/habitat_edits/v29_v30/gmw_hab_v29_add.geojson"
in_rm_vec_file = "/Users/pfb/Library/CloudStorage/Dropbox/University/Research/Data/Mangroves/GMW_Habitat_Layers/habitat_edits/v29_v30/gmw_hab_v29_rm.geojson"


out_add_vec_file = "gmw_v30_hab_add.geojson"
out_add_vec_lyr = "gmw_v30_hab_add"
out_rm_vec_file = "gmw_v30_hab_rm.geojson"
out_rm_vec_lyr = "gmw_v30_hab_rm"


rsgislib.vectorutils.merge_vector_files(
    vec_files=[in_add_vec_file],
    out_vec_file=out_add_vec_file,
    out_vec_lyr=out_add_vec_lyr,
    out_format="GeoJSON",
    out_epsg=None,
    remove_cols=None,
)

rsgislib.vectorutils.merge_vector_files(
    vec_files=[in_rm_vec_file],
    out_vec_file=out_rm_vec_file,
    out_vec_lyr=out_rm_vec_lyr,
    out_format="GeoJSON",
    out_epsg=None,
    remove_cols=None,
)
