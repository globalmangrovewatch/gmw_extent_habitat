import os
import shutil
import rsgislib.tools.utils
import rsgislib.tools.filetools

cop_30_dem_path = "/bigdata/petebunting/copernicus-dem-30m/copernicus-dem-30m"
out_cop_30_dem_path = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_dwnld_tiles"
if not os.path.exists(out_cop_30_dem_path):
    os.mkdir(out_cop_30_dem_path)

out_cop_30_dem_ext_path = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_extract_tiles"
if not os.path.exists(out_cop_30_dem_ext_path):
    os.mkdir(out_cop_30_dem_ext_path)

cop_dem_tiles = rsgislib.tools.utils.read_text_file_to_list("cop_30_dem_gmw_tiles.txt")

for cop_dem_tile in cop_dem_tiles:
    in_cop_file = os.path.join(cop_30_dem_path, cop_dem_tile)
    if os.path.exists(in_cop_file):
        shutil.copy2(in_cop_file, out_cop_30_dem_path)
        lcl_cop_file = os.path.join(out_cop_30_dem_path, cop_dem_tile)

        rsgislib.tools.filetools.untar_file(lcl_cop_file, out_cop_30_dem_ext_path, gen_arch_dir = False, verbose = False)
        break