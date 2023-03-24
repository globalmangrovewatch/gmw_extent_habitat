import os
import shutil
import tqdm
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
failed_scns = list()
for cop_dem_tile in tqdm.tqdm(cop_dem_tiles):
    in_cop_file = os.path.join(cop_30_dem_path, cop_dem_tile)
    if os.path.exists(in_cop_file):
        lcl_cop_file = os.path.join(out_cop_30_dem_path, cop_dem_tile)
        if not os.path.exists(lcl_cop_file):
            shutil.copy2(in_cop_file, out_cop_30_dem_path)

        scn_basename = rsgislib.tools.filetools.get_file_basename(lcl_cop_file)
        cop_scn_dir = os.path.join(out_cop_30_dem_ext_path, scn_basename)
        if not os.path.exists(cop_scn_dir):
            try:
                rsgislib.tools.filetools.untar_file(lcl_cop_file, out_cop_30_dem_ext_path, gen_arch_dir = False, verbose = False)
            except:
                print(cop_dem_tile)
                failed_scns.append(cop_dem_tile)
print(failed_scns)
rsgislib.tools.utils.write_list_to_file(failed_scns, "fails.txt")
print("HERE")

