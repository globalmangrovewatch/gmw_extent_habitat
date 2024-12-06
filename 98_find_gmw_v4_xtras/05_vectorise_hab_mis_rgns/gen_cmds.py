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

        cmp_process_dir = "cmp_process_chk"
        if not os.path.exists(cmp_process_dir):
            os.mkdir(cmp_process_dir)

        imgs = glob.glob(kwargs["hab_mis_imgs"])

        for img in imgs:
            basename = rsgislib.tools.filetools.get_file_basename(img)
            out_vec_lyr = f"{basename}_vec"
            out_vec_file = os.path.join(kwargs["out_dir"], f"{out_vec_lyr}.gpkg")
            out_cmp_file = os.path.join(cmp_process_dir, f"{basename}_cmp.txt")
            if not os.path.exists(out_cmp_file):
                c_dict = dict()
                c_dict["hab_mis_img"] = img
                c_dict["out_vec_lyr"] = out_vec_lyr
                c_dict["out_vec_file"] = out_vec_file
                c_dict["out_cmp_file"] = out_cmp_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(hab_mis_imgs="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_v4021_mis_hab_tiles/*.kea",
                out_dir="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_v4021_mis_hab_tiles_vec")

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",  # The file to call to run analysis
            cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
            n_cores=25,  # The number of cores to use for analysis.
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
