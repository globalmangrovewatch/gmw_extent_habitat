import os
import rsgislib.tools.utils
import rsgislib.tools.httptools
import rsgislib.tools.filetools

scn_urls = rsgislib.tools.utils.read_text_file_to_list("cop_30_dem_gmw_tiles_urls_dwnld.txt")
out_file_path = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_dwnld_ext_tiles"

for scn_url in scn_urls:
    print(scn_url)
    file_name = os.path.basename(scn_url)
    scn_path = os.path.join(out_file_path, file_name)
    print(scn_path)
    rsgislib.tools.httptools.download_file_http(scn_url, scn_path, no_except = True)