import logging
import os
import rsgislib.vectorutils.createrasters

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        rsgislib.vectorutils.createrasters.rasterise_vec_lyr(
            self.params["gmw_vec_file"],
            self.params["gmw_vec_lyr"],
            input_img=self.params["base_img"],
            output_img=self.params["gmw_ext_img"],
            gdalformat="KEA",
            burn_val=1,
            datatype=rsgislib.TYPE_8UINT,
            att_column=None,
            use_vec_extent=False,
            thematic=True,
            no_data_val=0,
        )

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "base_img",
            "gmw_vec_file",
            "gmw_vec_lyr",
            "gmw_ext_img",
        ]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["gmw_ext_img"]] = "gdal_image"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files and reset anything
        # else which might need to be reset if re-running the job.
        if os.path.exists(self.params["gmw_ext_img"]):
            os.remove(self.params["gmw_ext_img"])


if __name__ == "__main__":
    ProcessCmd().std_run()

