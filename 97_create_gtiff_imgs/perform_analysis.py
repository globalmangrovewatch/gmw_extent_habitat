import logging
import os
import rsgislib.imagecalc
import subprocess

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        hab_pxls = rsgislib.imagecalc.count_pxls_of_val(self.params["img"], vals =[1], img_band = 1)[0]
        print(f"hab_pxls = {hab_pxls}")
        if hab_pxls > 0:
            cmd = (
                "gdal_translate -of COG -co COMPRESS=LZW "
                "-co OVERVIEW_RESAMPLING=NEAREST  {} {}".format(
                    self.params["img"], self.params["out_img"]
                )
            )
            print("Running: '{}'".format(cmd))
            try:
                subprocess.check_call(cmd, shell=True)
            except OSError as e:
                raise Exception("Could not execute command: {}".format(cmd))

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "img",
            "out_img",
        ]

    def outputs_present(self, **kwargs):
        # Check the output files are as expected - called with --check option
        # the function expects a tuple with the first item a list of booleans
        # specifying whether the file is OK and secondly a dict with outputs
        # as keys and any error message as the value

        # A function (self.check_files) has been provided to do the work for
        # you which takes a dict of inputs which will do the work for you in
        # most cases. The supported file types are: gdal_image, gdal_vector,
        # hdf5, file (checks present) and filesize (checks present and size > 0)

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

