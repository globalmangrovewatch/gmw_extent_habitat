import logging
import os
import rsgislib
import rsgislib.imagecalc
import rsgislib.rastergis

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw_v3', self.params["gmw_v4_ext_img"], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw_v4', self.params["gmw_v3_ext_img"], 1))
        rsgislib.imagecalc.band_math(self.params["gmw_merged_ext"], '(gmw_v3==1)&&(gmw_v4==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.pop_rat_img_stats(clumps_img=self.params["gmw_merged_ext"], add_clr_tab=True, calc_pyramids=True, ignore_zero=True)

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "gmw_v4_ext_img",
            "gmw_v3_ext_img",
            "gmw_merged_ext",
        ]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["gmw_merged_ext"]] = "gdal_image"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files and reset anything
        # else which might need to be reset if re-running the job.
        if os.path.exists(self.params["gmw_merged_ext"]):
            os.remove(self.params["gmw_merged_ext"])

if __name__ == "__main__":
    ProcessCmd().std_run()

