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

        base_tiles = glob.glob(kwargs["base_tiles"])
        for base_img in base_tiles:
            basename = rsgislib.tools.filetools.get_file_basename(base_img)
            gmw_hab_img = os.path.abspath(os.path.join(kwargs["gmw_hab_msk"], f"gmw_{basename}_hab_v21.kea"))
            gmw_v4_img = os.path.join(kwargs["gmw_fnl_dir"], f"{basename}_gmw_v4.kea")
            out_img = os.path.join(kwargs["out_dir"], f"{basename}_gmw_v4_hab_mis.kea")
            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict["gmw_hab_img"] = gmw_hab_img
                c_dict["gmw_v4_img"] = gmw_v4_img
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
            base_tiles="../../01_gmw_tiles/base_tiles/*.tif",
            gmw_hab_msk="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_hab_v21_tiles/",
            gmw_fnl_dir="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_v4021_tiles",
            out_dir="/bigdata/petebunting/GlobalMangroveWatch/gmw_hab_extent/data/gmw_v4021_mis_hab_tiles",
        )

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",  # The file to call to run analysis
            cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
            n_cores=50,  # The number of cores to use for analysis.
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
