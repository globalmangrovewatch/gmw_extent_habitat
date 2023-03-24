import rsgislib.tools.filetools
import rsgislib.tools.utils
import shutil

scns_path = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_extract_tiles"

scns_lst = rsgislib.tools.filetools.get_dir_list(scns_path)
rmd_scns = list()
for scn_path in scns_lst:
    scn_dir = rsgislib.tools.filetools.get_dir_name(scn_path)
    #print(scn_dir)
    scn_dem = rsgislib.tools.filetools.find_file_none(scn_path, "DEM/*.tif")
    if scn_dem is None:
        print(scn_path)
        rmd_scns.append(scn_dir)
        #shutil.rmtree(scn_path)

rsgislib.tools.utils.write_list_to_file(rmd_scns, "cop_30_dem_gmw_tiles_rmd.txt")

