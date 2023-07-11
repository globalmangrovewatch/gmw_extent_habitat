import rsgislib.vectorutils


hab_add_files =["/Users/pete/Dropbox/University/Research/Data/Mangroves/GMW_Habitat_Layers/habitat_edits/v13_v14/gmw_hab_v13_add_2.gpkg",
                "/Users/pete/Dropbox/University/Research/Data/Mangroves/GMW_Habitat_Layers/habitat_edits/v13_v14/gmw_hab_v13_add.gpkg",
                "/Users/pete/Development/globalmangrovewatch/gmw_v4_baseline_cls/15_gmw_v4_007_qa/ake_qa/QA_Caribeean-West_100723/v4.007_Missing_Habitat_Caribbean-West.shp",
                "/Users/pete/Development/globalmangrovewatch/gmw_v4_baseline_cls/15_gmw_v4_007_qa/ake_qa/QA_Caribeean-East_070723/v4.007_Missing_Habitat_Caribbean-East.shp",
                "/Users/pete/Development/globalmangrovewatch/gmw_define_v4_training/22_further_train_qa/lammert_edits/gmw_hab_mask_v13-missing_areas.gpkg"]

rsgislib.vectorutils.merge_vector_files(hab_add_files, out_vec_file="gmw_v13_hab_add.geojson", out_vec_lyr = None, out_format = 'GeoJSON', out_epsg = None)


hab_rm_files = ["/Users/pete/Dropbox/University/Research/Data/Mangroves/GMW_Habitat_Layers/habitat_edits/v13_v14/gmw_hab_v13_rm.gpkg"]

rsgislib.vectorutils.merge_vector_files(hab_rm_files, out_vec_file="gmw_v13_hab_rm.geojson", out_vec_lyr = None, out_format = 'GeoJSON', out_epsg = None)

