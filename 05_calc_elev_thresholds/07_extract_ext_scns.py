import os
import glob
import rsgislib.tools.filetools

ext_scn_path = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_dwnld_ext_tiles"
ext_scn_extract_path = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_extract_ext_tiles"

if not os.path.exists(ext_scn_extract_path):
    os.mkdir(ext_scn_extract_path)

scns_tar_lst = glob.glob(os.path.join(ext_scn_path, "*.tar"))

for scn_tar in scns_tar_lst:
    print(scn_tar)
    scn_basename = rsgislib.tools.filetools.get_file_basename(scn_tar)
    cop_scn_dir = os.path.join(ext_scn_extract_path, scn_basename)

    if not os.path.exists(cop_scn_dir):
        try:
            rsgislib.tools.filetools.untar_file(scn_tar, ext_scn_extract_path, gen_arch_dir=False, verbose=False)
        except:
            print(scn_tar)

