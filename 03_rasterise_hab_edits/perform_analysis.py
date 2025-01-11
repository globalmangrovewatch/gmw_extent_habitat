import logging
import os
import rsgislib.imageutils
import rsgislib.vectorutils.createrasters
import rsgislib.rastergis

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        rsgislib.vectorutils.createrasters.rasterise_vec_lyr(
            vec_file=self.params["vec_file"],
            vec_lyr=self.params["vec_lyr"],
            input_img=self.params["ref_img"],
            output_img=self.params["out_img"],
            gdalformat="KEA",
            burn_val=1,
            datatype=rsgislib.TYPE_8UINT,
            att_column=None,
            use_vec_extent=False,
            thematic=True,
            no_data_val=0,
        )

        rsgislib.rastergis.pop_rat_img_stats(
            clumps_img=self.params["out_img"],
            add_clr_tab=True,
            calc_pyramids=True,
            ignore_zero=True,
            rat_band=1,
        )
        """
        rsgislib.imageutils.pop_thmt_img_stats(
            self.params["out_img"],
            add_clr_tab=True,
            calc_pyramids=True,
            ignore_zero=True,
        )
        """

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "ref_img",
            "vec_file",
            "vec_lyr",
            "out_img",
        ]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_img"]] = "gdal_image"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files and reset anything
        # else which might need to be reset if re-running the job.
        if os.path.exists(self.params["out_img"]):
            os.remove(self.params["out_img"])


if __name__ == "__main__":
    ProcessCmd().std_run()
