import rsgislib.tools.filetools
import shutil

scns_path = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_extract_tiles"

scns_lst = rsgislib.tools.filetools.get_dir_list(scns_path)

for scn_path in scns_lst:
    print(scn_path)
    scn_dir = rsgislib.tools.filetools.get_dir_name(scn_path)
    print(scn_dir)
    #scn_dem = rsgislib.tools.filetools.find_file_none(scn_path, "DEM/*.tif")
    #if scn_dem is None:
    #    shutil.rmtree(scn_path)