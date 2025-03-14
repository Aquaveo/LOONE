import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class M_var:
    """Class to represents model variables."""
    def __init__(self, config: dict, forecast: bool = False):
        """
        Initializes the M_var class with model variables.

        This constructor sets up various model variables and arrays based on the provided configuration dictionary.
        It calculates date ranges and initializes arrays for different time scales (daily, weekly, monthly)
        and model parameters, including tributary conditions, seasonal classes, lake stages, supply, and outflows.

        Args:
            config (dict): A dictionary containing configuration parameters, including:
                - "start_date_entry": A list of integers [year, month, day] for the start date.
                - "end_date_entry": A list of integers [year, month, day] for the end date.
                - "end_date_tc": A list of integers [year, month, day] for the end date of tributary conditions.
                - "month_n": An integer representing the number of months for the LONINO seasonal classes.
        """
        if forecast==True:
            today = datetime.today().date()
            startdate = today
            enddate = today + timedelta(days=15)
        else:
            year, month, day = map(int, config["start_date_entry"])
            startdate = datetime(year, month, day).date()
            year, month, day = map(int, config["end_date_entry"])
            enddate = datetime(year, month, day).date()
        year, month, day = map(int, config["end_date_tc"])
        enddate_TC = datetime(year, month, day).date()

        date_rng_3 = pd.date_range(
            start=startdate, end=enddate_TC, freq="W-Fri"
        )
        TC_Count = len(date_rng_3)
        self.RF_Cls = np.zeros(TC_Count)
        self.MainTrib_Cls = np.zeros(TC_Count)
        self.Palmer_Cls = np.zeros(TC_Count)
        self.NetInflow_Cls = np.zeros(TC_Count)
        self.Max_RF_MainTrib = np.zeros(TC_Count)
        self.Max_Palmer_NetInf = np.zeros(TC_Count)

        date_rng_4 = pd.date_range(start=startdate, end=enddate, freq="MS")
        if date_rng_4.empty:
            date_rng_4  = pd.DatetimeIndex([pd.to_datetime(startdate).replace(day=1)])
        LONINO_Count = len(date_rng_4)
        self.Seas = np.zeros(LONINO_Count)
        self.M_Seas = np.zeros(LONINO_Count)
        self.LONINO_Seas_cls = np.zeros(config["month_n"])
        self.LONINO_M_Seas_cls = np.zeros(config["month_n"])

        date_rng_5 = pd.date_range(start=startdate, end=enddate, freq="D")
        Seas_Count = len(date_rng_5)
        self.Daily_Seasons = np.zeros(Seas_Count)
        self.Mon = np.zeros(Seas_Count)

        date_rng_6 = pd.date_range(
            start=startdate - timedelta(days=1),
            end=enddate,
            freq="D",
        )
        n_rows = len(date_rng_6)
        self.Lake_Stage = np.zeros(n_rows, dtype=object)
        self.WSM_Zone = np.zeros(n_rows, dtype=object)
        self.Max_Supply = np.zeros(n_rows, dtype=object)
        self.LOSA_Supply = np.zeros(n_rows, dtype=object)
        self.Cut_back = np.zeros(n_rows, dtype=object)
        self.Dem_N_Sup = np.zeros(n_rows, dtype=object)

        V = len(date_rng_5)
        self.V10per = np.zeros(V)
        self.V20per = np.zeros(V)
        self.V25per = np.zeros(V)
        self.V30per = np.zeros(V)
        self.V40per = np.zeros(V)
        self.V45per = np.zeros(V)
        self.V50per = np.zeros(V)
        self.V60per = np.zeros(V)
        self.NI_Supply = np.zeros(n_rows, dtype=object)
        self.Zone_Code = np.zeros(n_rows, dtype=object)
        self.LO_Zone = np.zeros(n_rows, dtype=object)

        Counter = len(date_rng_5)
        self.Zone_D_Trib = np.zeros(Counter)
        self.Zone_D_stage = np.zeros(Counter)
        self.Zone_D_Seas = np.zeros(Counter)
        self.Zone_D_MSeas = np.zeros(Counter)
        self.Zone_D_Branch_Code = np.zeros(Counter)
        self.Zone_D_Rel_Code = np.zeros(Counter)
        self.Zone_C_Trib = np.zeros(Counter)
        self.Zone_C_Seas = np.zeros(Counter)
        self.Zone_C_MSeas = np.zeros(Counter)
        self.Zone_C_MetFcast = np.zeros(Counter)
        self.Zone_C_Branch_Code = np.zeros(Counter)
        self.Zone_C_Rel_Code = np.zeros(Counter)
        self.Zone_B_Trib = np.zeros(Counter)
        self.Zone_B_Stage = np.zeros(Counter)
        self.Zone_B_Seas = np.zeros(Counter)
        self.Zone_B_Branch_Code = np.zeros(Counter)
        self.Zone_B_Rel_Code = np.zeros(Counter)
        self.DecTree_Relslevel = np.zeros(n_rows, dtype=object)
        self.DayFlags = np.zeros(n_rows, dtype=object)
        self.PlsDay = np.zeros(n_rows, dtype=object)
        self.Release_Level = np.zeros(n_rows, dtype=object)
        self.dh_7days = np.zeros(n_rows, dtype=object)
        self.ZoneCodeminus1Code = np.zeros(n_rows, dtype=object)
        self.ZoneCodeCode = np.zeros(n_rows, dtype=object)
        self.Fraction_of_Zone_height = np.zeros(n_rows, dtype=object)
        self.ReLevelCode_1 = np.zeros(n_rows, dtype=object)
        self.ReLevelCode_2 = np.zeros(n_rows, dtype=object)
        self.ReLevelCode_3_S80 = np.zeros(n_rows, dtype=object)
        self.Outlet2DS_Mult = np.zeros(n_rows, dtype=object)
        self.Outlet2DS_Mult_2 = np.zeros(n_rows, dtype=object)
        self.Outlet2DSRS = np.zeros(n_rows, dtype=object)
        self.Outlet2USRG1 = np.zeros(n_rows, dtype=object)
        self.Sum_Outlet2USRG1 = np.zeros(n_rows, dtype=object)
        self.Outlet2DSBS = np.zeros(n_rows, dtype=object)
        self.Outlet2USBK = np.zeros(n_rows, dtype=object)
        self.ROeast = np.zeros(n_rows, dtype=object)
        self.Outlet2USBS = np.zeros(n_rows, dtype=object)
        self.Sum_Outlet2USBK = np.zeros(n_rows, dtype=object)
        self.Outlet2USRG_Code = np.zeros(n_rows, dtype=object)
        self.Outlet2USRG = np.zeros(n_rows, dtype=object)
        self.Outlet2DS = np.zeros(n_rows, dtype=object)
        self.ReLevelCode_3_S77 = np.zeros(n_rows, dtype=object)
        self.Outlet1US_Mult = np.zeros(n_rows, dtype=object)
        self.Outlet1US_Mult_2 = np.zeros(n_rows, dtype=object)
        self.Outlet1USBSAP = np.zeros(n_rows, dtype=object)
        self.Outlet1USRS = np.zeros(n_rows, dtype=object)
        self.Sum_Outlet1USRS = np.zeros(n_rows, dtype=object)
        self.Outlet1USBK = np.zeros(n_rows, dtype=object)
        self.ROwest = np.zeros(n_rows, dtype=object)
        self.Outlet1DSBS = np.zeros(n_rows, dtype=object)
        self.Outlet1USBS = np.zeros(n_rows, dtype=object)
        self.Outlet1USEWS = np.zeros(n_rows, dtype=object)
        self.Outlet1USREG = np.zeros(n_rows, dtype=object)
        self.Outlet1DS = np.zeros(n_rows, dtype=object)
        self.TotRegEW = np.zeros(n_rows, dtype=object)
        self.Choose_WCA = np.zeros(n_rows, dtype=object)
        self.RegWCA = np.zeros(n_rows, dtype=object)
        self.Choose_L8C51 = np.zeros(n_rows, dtype=object)
        self.RegL8C51 = np.zeros(n_rows, dtype=object)
        self.TotRegSo = np.zeros(n_rows, dtype=object)
        self.Stage2ar = np.zeros(n_rows, dtype=object)
        self.Stage2marsh = np.zeros(n_rows, dtype=object)
        self.RF = np.zeros(n_rows, dtype=object)
        self.ET = np.zeros(n_rows, dtype=object)
        self.Choose_WSA_1 = np.zeros(n_rows, dtype=object)
        self.Choose_WSA_2 = np.zeros(n_rows, dtype=object)
        self.WSA_MIA = np.zeros(n_rows, dtype=object)
        self.WSA_NNR = np.zeros(n_rows, dtype=object)
        self.DSto = np.zeros(n_rows, dtype=object)
        self.Storage = np.zeros(n_rows, dtype=object)

        Count_AP = len(date_rng_5)
        self.THC_Class_normal_or_above = np.zeros(Count_AP)
        self.Lake_O_Stage_AP = np.zeros(Count_AP)
        self.Lake_O_Schedule_Zone = np.zeros(Count_AP)
        self.LStgCorres = np.zeros(Count_AP)
        self.LowChance_Check = np.zeros(Count_AP)
        self.Outlet1USRS_AP = np.zeros(Count_AP)
        self.Outlet1USBS_AP = np.zeros(Count_AP)
        self.Outlet1USRS_Pre_AP_S77_Baseflow = np.zeros(Count_AP)
        self.Forecast_D_Sal = np.zeros(Count_AP)
        self.n30d_mavg = np.zeros(Count_AP)
        self.n30davgForecast = np.zeros(Count_AP)
        self.LORS08_bf_rel = np.zeros(Count_AP)
        self.LDS_LC6_1 = np.zeros(Count_AP)
        self.S_O = np.zeros(Count_AP)
        self.All_4 = np.zeros(Count_AP)
        self.Sabf = np.zeros(Count_AP)
        self.Swbf = np.zeros(Count_AP)
        self.Swbu = np.zeros(Count_AP)
        self.All_4andStage = np.zeros(Count_AP)
        self.All_4andStagein = np.zeros(Count_AP)
        self.P_AP_BF_Stg = np.zeros(Count_AP)
        self.Logic_test_1 = np.zeros(Count_AP)
        self.Post_Ap_Baseflow = np.zeros(Count_AP)
        self.Outlet1USRSplusPreAPS77bsf = np.zeros(Count_AP)
        self.AndEstNeedsLakeWater = np.zeros(Count_AP)
        self.Choose_PAPEWS_1 = np.zeros(Count_AP)
        self.Choose_PAPEWS_2 = np.zeros(Count_AP)
        self.AndLowChance61stagelessth11 = np.zeros(Count_AP)
        self.ATHCnora = np.zeros(Count_AP)
        self.Post_AP_EWS = np.zeros(Count_AP)
        self.Post_AP_Baseflow_EWS_cfs = np.zeros(Count_AP)
