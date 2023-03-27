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
            gmw_ext_img = os.path.join(kwargs["out_dir"], f"{gmw_tile_basename}_v4_002_ext.kea")
            if not os.path.exists(gmw_ext_img):
                c_dict = dict()
                c_dict["base_img"] = base_img
                c_dict["gmw_vec_file"] = kwargs["vec_file"]
                c_dict["gmw_vec_lyr"] = kwargs["vec_lyr"]
                c_dict["gmw_ext_img"] = gmw_ext_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(base_img_tiles="../../01_gmw_tiles/base_tiles/*.tif",
                              vec_file="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_v4_sen2_sgl_cls_v002.gpkg",
                              vec_lyr="gmw_v4_sen2_sgl_cls_v002",
            out_dir="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_tile_v4_002_ext")

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",  # The file to call to run analysis
            cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
            n_cores=20,  # The number of cores to use for analysis.
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

