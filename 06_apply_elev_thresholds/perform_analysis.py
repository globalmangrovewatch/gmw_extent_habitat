import logging
import os
import rsgislib.imagecalc
import rsgislib.rastergis

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        if self.params["dem_img"] != "":
            band_defns = list()
            band_defns.append(rsgislib.imagecalc.BandDefn("hab", self.params["hab_img"], 1))
            band_defns.append(rsgislib.imagecalc.BandDefn("dem", self.params["dem_img"], 1))
            exp = f"(hab==1)&&(dem<{self.params['elev_thres']})?1:0"
            rsgislib.imagecalc.band_math(
                self.params["new_hab_img"], exp, "KEA", rsgislib.TYPE_8UINT, band_defns
            )
        else:
            band_defns = list()
            band_defns.append(rsgislib.imagecalc.BandDefn("hab",
                                                          self.params["hab_img"], 1))
            rsgislib.imagecalc.band_math(
                self.params["new_hab_img"], "hab", "KEA", rsgislib.TYPE_8UINT, band_defns
                )
        rsgislib.rastergis.pop_rat_img_stats(
            clumps_img=self.params["new_hab_img"],
            add_clr_tab=True,
            calc_pyramids=True,
            ignore_zero=True,
        )

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "hab_img",
            "dem_img",
            "elev_thres",
            "new_hab_img",
        ]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["new_hab_img"]] = "gdal_image"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files and reset anything
        # else which might need to be reset if re-running the job.
        if os.path.exists(self.params["new_hab_img"]):
            os.remove(self.params["new_hab_img"])


if __name__ == "__main__":
    ProcessCmd().std_run()
