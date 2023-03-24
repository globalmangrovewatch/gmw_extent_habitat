import rsgislib.tools.utils
import rsgislib.tools.httptools

scn_urls = rsgislib.tools.utils.read_text_file_to_list("cop_30_dem_gmw_tiles_urls_dwnld.txt")
out_file_path = "/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/cop30_dwnld_ext_tiles"

for scn_url in scn_urls:
    print(scn_url)
    rsgislib.tools.httptools.download_file_http(scn_url, out_file_path, no_except = True)