import os
import pandas as pd
from loone.utils import load_config


class Data:
    """A class that represents the data used for running LOONE."""

    def __init__(self, working_path: str):
        """
        Initializes the Data object.

        Args:
            working_path (str): The working directory path.
        """
        # Load the configuration
        config = load_config(working_path)
        self.data_dir = working_path

        # Read the data from the configuration
        self.read_data(config)

    def read_data(self, config: dict) -> None:
        """
        Reads all the data from the configuration files.

        Args:
            config (dict): The configuration dictionary.
        """
        self.SFWMM_Daily_Outputs = self._read_csv(
            config, "sfwmm_daily_outputs"
        )
        self.WSMs_RSBKs = self._read_csv(config, "wsms_rsbps")
        self.Weekly_dmd = self._read_csv(config, "losa_wkly_dmd")
        self.Wkly_Trib_Cond = self._read_csv(config, "trib_cond_wkly_data")
        self.LONINO_Seas_data = self._read_csv(config, "seasonal_lonino")
        self.LONINO_Mult_Seas_data = self._read_csv(
            config, "multi_seasonal_lonino"
        )
        self.NetInf_Input = self._read_csv(config, "netflows_acft")
        self.SFWMM_W_dmd = self._read_csv(config, "water_dmd")
        self.RF_Vol = self._read_csv(config, "rf_vol")
        self.ET_Vol = self._read_csv(config, "et_vol")
        self.C44_Runoff = self._read_csv(config, "c44ro")
        self.C43RO_Daily = self._read_csv(config, "c43ro")
        self.Sum_Basin_RO = self._read_csv(config, "basin_ro_inputs")
        self.C43RO = self._read_csv(config, "c43ro_monthly")
        self.C44RO = self._read_csv(config, "c44ro_nonthly")
        self.SLTRIB = self._read_csv(config, "sltrib_monthly")
        self.S80_RegRelRates = self._read_csv(
            config, "s80_regulatory_release_rates"
        )
        self.S77_RegRelRates = self._read_csv(
            config, "s77_regulatory_release_rates"
        )
        self.CE_SLE_turns = self._read_csv(config, "ce_sle_turns_inputs")
        self.Pulses = self._read_csv(config, "pulses_inputs")
        self.Targ_Stg_May_1st = self._read_csv(
            config, "may_1st_lake_stage_below_11ft", parse_dates=["Date"]
        )
        self.Targ_Stg_June_1st = self._read_csv(
            config, "june_1st_lake_stage_below_11ft", parse_dates=["Date"]
        )
        self.Estuary_needs_water = self._read_csv(
            config, "estuary_needs_water_input"
        )
        self.EAA_MIA_RUNOFF = self._read_csv(config, "eaa_mia_ro_inputs")
        self.Storage_dev_df = self._read_csv(config, "storage_deviation")
        self.Cal_Par = self._read_csv(config, "calibration_parameters")

    def _read_csv(self, config: dict, key: str, **kwargs) -> pd.DataFrame:
        """
        Helper function to construct the file path and read the CSV file.

        Args:
            config (dict): The configuration dictionary.
            key (str): The key to look up the file path in the configuration.
            **kwargs: Additional arguments to pass to pd.read_csv.

        Returns:
            pd.DataFrame: The loaded DataFrame.
        """
        file_path = os.path.join(self.data_dir, config[key])
        return pd.read_csv(file_path, **kwargs)
