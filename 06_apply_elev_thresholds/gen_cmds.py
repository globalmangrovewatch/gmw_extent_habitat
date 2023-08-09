import logging
import os
import glob

import rsgislib.tools.filetools
import rsgislib.tools.utils

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        # Create output directory if it doesn't exist.
        if not os.path.exists(kwargs["out_dir"]):
            os.mkdir(kwargs["out_dir"])

        elev_thres_lut = rsgislib.tools.utils.read_json_to_dict(kwargs["dem_thres_lut"])

        base_imgs = glob.glob(kwargs["base_img_tiles"])
        for base_img in base_imgs:
            gmw_tile_basename = rsgislib.tools.filetools.get_file_basename(base_img)

            hab_img = os.path.join(
                kwargs["gmw_hab_dir"], f"gmw_{gmw_tile_basename}_hab_v14_tmp.kea"
            )
            dem_img = os.path.join(kwargs["dem_dir"], f"{gmw_tile_basename}_dem.kea")
            if os.path.exists(dem_img):
                if os.path.exists(hab_img):
                    new_hab_img = os.path.join(
                        kwargs["out_dir"], f"gmw_{gmw_tile_basename}_hab_v13.kea"
                    )
                    if not os.path.exists(new_hab_img):
                        c_dict = dict()
                        c_dict["hab_img"] = hab_img
                        c_dict["dem_img"] = dem_img
                        c_dict["elev_thres"] = elev_thres_lut[gmw_tile_basename]
                        c_dict["new_hab_img"] = new_hab_img
                        self.params.append(c_dict)
            else:
                print(f"Creating a job without a DEM: {gmw_tile_basename}")
                if os.path.exists(hab_img):
                    new_hab_img = os.path.join(
                        kwargs["out_dir"], f"gmw_{gmw_tile_basename}_hab_v13.kea"
                        )
                    if not os.path.exists(new_hab_img):
                        c_dict = dict()
                        c_dict["hab_img"] = hab_img
                        c_dict["dem_img"] = ""
                        c_dict["elev_thres"] = elev_thres_lut[gmw_tile_basename]
                        c_dict["new_hab_img"] = new_hab_img
                        self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
            base_img_tiles="../01_gmw_tiles/base_tiles/*.tif",
            gmw_hab_dir="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/scripts/04_apply_edits/gmw_hab_tiles",
            dem_dir="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_cop30_dem",
            dem_thres_lut="../05_calc_elev_thresholds/gmw_v3_v4_inter_elev_tile_fnl_thresholds.json",
            out_dir="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_hab_v14_tiles",
        )

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",  # The file to call to run analysis
            cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
            n_cores=10,  # The number of cores to use for analysis.
            db_info_file="pbpt_lcl_db_info.json",
        )


if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = f"python {py_script}"

    process_tools_mod = "perform_analysis"
    process_tools_cls = "ProcessCmd"

    create_tools = GenCmds(
        cmd=script_cmd,
        db_conn_file="/home/pete/.pbpt_db_conn.txt",
        lock_file_path="./pbpt_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
    )
    create_tools.parse_cmds()
