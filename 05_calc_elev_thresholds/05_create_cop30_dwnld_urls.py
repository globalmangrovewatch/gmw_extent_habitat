import os
import rsgislib.tools.utils
import rsgislib.tools.filetools

cop30_scn_urls = rsgislib.tools.utils.read_json_to_dict("cop_dem_glo_30_urls.json")

scn_lut = dict()
for cop30_scn in cop30_scn_urls:
    print(cop30_scn["nativeDemUrl"])
    scn_name = rsgislib.tools.filetools.get_file_basename(cop30_scn["nativeDemUrl"])
    print(f"\t{scn_name}")
    scn_lut[scn_name] = cop30_scn["nativeDemUrl"]

scn_dnwld = list()

fail1_tiles = rsgislib.tools.utils.read_text_file_to_list(
    "cop_30_dem_gmw_tiles_fails.txt"
)
fail2_tiles = rsgislib.tools.utils.read_text_file_to_list(
    "cop_30_dem_gmw_tiles_not_avail.txt"
)
fail3_tiles = rsgislib.tools.utils.read_text_file_to_list(
    "cop_30_dem_gmw_tiles_rmd.txt"
)
fail_tiles = fail1_tiles + fail2_tiles + fail3_tiles
for tile in fail_tiles:
    if "." in tile:
        tile = os.path.splitext(tile)[0]
    print(tile)

    if tile in scn_lut:
        scn_dnwld.append(scn_lut[tile])

rsgislib.tools.utils.write_list_to_file(
    scn_dnwld, "cop_30_dem_gmw_tiles_urls_dwnld.txt"
)
