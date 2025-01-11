import rsgislib.vectorutils

vec_files = ["/Users/pete/Dropbox/University/Research/Data/Mangroves/GMW_Habitat_Layers/habitat_edits/v25_v26/gmw_hab_msk_v24_missing_areas-b.gpkg", "/Users/pete/Dropbox/University/Research/Data/Mangroves/GMW_Habitat_Layers/habitat_edits/v25_v26/gmw_hab_v25_add.geojson"]

rsgislib.vectorutils.merge_vector_files(vec_files, out_vec_file = "gmw_v26_hab_add.geojson", out_vec_lyr = "gmw_v26_hab_add", out_format = 'GeoJSON', out_epsg = None, remove_cols = None)