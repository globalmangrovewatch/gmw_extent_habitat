import rsgislib.vectorutils


hab_add_files =["/Users/pete/Dropbox/University/Research/Data/Mangroves/GMW_Habitat_Layers/habitat_edits/v14_v15/gmw_hab_v14_add.gpkg"]
rsgislib.vectorutils.merge_vector_files(hab_add_files, out_vec_file="gmw_v15_hab_add.geojson", out_vec_lyr = None, out_format = 'GeoJSON', out_epsg = None)


hab_rm_files = ["/Users/pete/Dropbox/University/Research/Data/Mangroves/GMW_Habitat_Layers/habitat_edits/v14_v15/gmw_hab_v14_rm.gpkg"]
rsgislib.vectorutils.merge_vector_files(hab_rm_files, out_vec_file="gmw_v15_hab_rm.geojson", out_vec_lyr = None, out_format = 'GeoJSON', out_epsg = None)

