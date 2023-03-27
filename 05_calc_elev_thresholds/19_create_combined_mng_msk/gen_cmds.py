import logging
import os
import glob
import rsgislib.tools.filetools

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        # Create output directory if it doesn't exist.
        if not os.path.exists(kwargs["out_dir"]):
            os.mkdir(kwargs["out_dir"])

        base_imgs = glob.glob(kwargs["base_img_tiles"])
        for base_img in base_imgs:
            gmw_tile_basename = rsgislib.tools.filetools.get_file_basename(base_img)
            gmw_v4_ext_img = os.path.join(kwargs["gmw_v4_tile"], f"{gmw_tile_basename}_v4_002_ext.kea")
            gmw_v3_ext_img = os.path.join(kwargs["gmw_v3_tile"], f"{gmw_tile_basename}_v3_2015_ext.kea")
            gmw_merged_ext = os.path.join(kwargs["out_dir"], f"{gmw_tile_basename}_v3_v4_inter_ext.kea")
            if not os.path.exists(gmw_merged_ext):
                c_dict = dict()
                c_dict["gmw_v4_ext_img"] = gmw_v4_ext_img
                c_dict["gmw_v3_ext_img"] = gmw_v3_ext_img
                c_dict["gmw_merged_ext"] = gmw_merged_ext
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(base_img_tiles="../../01_gmw_tiles/base_tiles/*.tif",
                              gmw_v4_tile="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_v4_002_ext",
                              gmw_v3_tile="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_v3_ext",
                              out_dir="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/mng_ext_gmw_v3_v4_002_inter")

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

