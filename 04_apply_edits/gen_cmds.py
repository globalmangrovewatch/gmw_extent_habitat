import logging
import os
import rsgislib.vectorattrs

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        # Create output directory if it doesn't exist.
        if not os.path.exists(kwargs["out_dir"]):
            os.mkdir(kwargs["out_dir"])

        tiles = rsgislib.vectorattrs.read_vec_column(
            vec_file=kwargs["gmw_tiles_vec_file"],
            vec_lyr=kwargs["gmw_tile_vec_lyr"],
            att_column="tile_name",
        )

        for tile in tiles:
            base_img = os.path.join(kwargs["gmw_base_tiles_dir"], f"{tile}.tif")
            hab_img = os.path.join(
                kwargs["old_hab_dir"],
                f"gmw_{tile}_hab_{kwargs['gmw_hab_prev_version']}.kea",
            )
            add_img = os.path.join(
                kwargs["add_dir"],
                f"gmw_{tile}_add_hab_{kwargs['gmw_hab_edit_version']}.tif",
            )
            rm_img = os.path.join(
                kwargs["rm_dir"],
                f"gmw_{tile}_rm_hab_{kwargs['gmw_hab_edit_version']}.tif",
            )

            out_img = os.path.join(
                kwargs["out_dir"],
                f"gmw_{tile}_hab_{kwargs['gmw_hab_new_version']}_tmp.kea",
            )
            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict["base_img"] = base_img
                c_dict["hab_img"] = hab_img
                c_dict["add_img"] = add_img
                c_dict["rm_img"] = rm_img
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
            gmw_base_tiles_dir="../01_gmw_tiles/base_tiles",
            add_dir="../03_rasterise_hab_edits/gmw_hab_adds",
            rm_dir="../03_rasterise_hab_edits/gmw_hab_rms",
            old_hab_dir="../../data/gmw_hab_v14_tiles",
            gmw_hab_prev_version="v14",
            gmw_hab_edit_version="v14_to_v15",
            gmw_hab_new_version="v15",
            gmw_tiles_vec_file="../01_gmw_tiles/gmw_degree_tiles.geojson",
            gmw_tile_vec_lyr="gmw_degree_tiles",
            out_dir="gmw_hab_tiles",
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
