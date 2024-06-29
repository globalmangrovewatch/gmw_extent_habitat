import rsgislib.vectorutils

edits_vec_file = ["/Users/pfb/Development/globalmangrovewatch/gmw_v4_baseline_cls/34_qa_4019/gmw_v4019_add_mng.geojson",
                  "/Users/pfb/Development/globalmangrovewatch/gmw_v4_baseline_cls/34_qa_4019/lammert/v4.019-add-to-mangrove.gpkg"]


rsgislib.vectorutils.merge_vector_files(edits_vec_file,
                                        out_vec_file = "gmw_v4_edits.gpkg",
                                        out_vec_lyr = "gmw_v4_edits",
                                        out_format = 'GPKG')
