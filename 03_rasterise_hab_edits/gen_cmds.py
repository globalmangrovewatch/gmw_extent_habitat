import logging
import os
import glob

import rsgislib.tools.filetools
import rsgislib.vectorattrs

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        # Create output directory if it doesn't exist.
        if not os.path.exists(kwargs["out_dir"]):
            os.mkdir(kwargs["out_dir"])

        tiles = rsgislib.vectorattrs.read_vec_column(
            vec_file=kwargs["tiles_vec_file"],
            vec_lyr=kwargs["tiles_vec_lyr"],
            att_column="tile_name",
        )

        for tile in tiles:
            base_img = os.path.join(kwargs["ref_img_dir"], f"{tile}.tif")
            out_img = os.path.join(
                kwargs["out_dir"], f"gmw_{tile}_{kwargs['out_img_end']}.kea"
            )
            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict["ref_img"] = base_img
                c_dict["vec_file"] = kwargs["edits_vec_file"]
                c_dict["vec_lyr"] = kwargs["edits_vec_lyr"]
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
            tiles_vec_file="../01_gmw_tiles/gmw_degree_tiles.geojson",
            tiles_vec_lyr="gmw_degree_tiles",
            ref_img_dir="../01_gmw_tiles/base_tiles",
            edits_vec_file="../00_edits/edits_v27_v28/gmw_v28_hab_add.geojson",
            edits_vec_lyr="gmw_v28_hab_add",
            out_img_end="add_hab_v26_to_v27",
            out_dir="gmw_hab_adds",
        )
        """
        self.gen_command_info(tiles_vec_file="../01_gmw_tiles/gmw_degree_tiles.geojson",
                              tiles_vec_lyr="gmw_degree_tiles",
                              ref_img_dir="../01_gmw_tiles/base_tiles",
                              edits_vec_file="../00_edits/edits_v26_v27/gmw_v27_hab_rm.geojson",
                              edits_vec_lyr="gmw_v27_hab_rm",
                              out_img_end="rm_hab_v26_to_v27",
                              out_dir="gmw_hab_rm")
        """

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
