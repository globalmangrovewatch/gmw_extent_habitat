import logging
import os
import pathlib

import rsgislib.imagecalc
import rsgislib.vectorutils.createvectors

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        pxl_vals = rsgislib.imagecalc.count_pxls_of_val(
            self.params["mng_img"], vals=[1], img_band=1
            )
        print(f"N Mangrove Pixels = {pxl_vals}")
        if pxl_vals[0] > 0:
            rsgislib.vectorutils.createvectors.polygonise_raster_to_vec_lyr(
                out_vec_file=self.params["out_vec_file"],
                out_vec_lyr=self.params["out_vec_lyr"],
                out_format="GPKG",
                input_img=self.params["mng_img"],
                img_band=1,
                mask_img=self.params["mng_img"],
                mask_band=1,
                replace_file=True,
                replace_lyr=True,
                pxl_val_fieldname="ClassID",
                use_8_conn=False,
                )
        pathlib.Path(self.params["out_cmp_file"]).touch()

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "mng_img",
            "out_vec_lyr",
            "out_vec_file",
            "out_cmp_file",
        ]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_vec_file"]] = "gdal_vector"
        files_dict[self.params["out_cmp_file"]] = "file"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files and reset anything
        # else which might need to be reset if re-running the job.
        if os.path.exists(self.params["out_vec_file"]):
            os.remove(self.params["out_vec_file"])
        if os.path.exists(self.params["out_cmp_file"]):
            os.remove(self.params["out_cmp_file"])


if __name__ == "__main__":
    ProcessCmd().std_run()

