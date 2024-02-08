import pandas as pd
from datetime import datetime
import numpy as np
from scipy import interpolate
from calendar import monthrange
import os
from Model_Config import Model_Config

Working_Path = Model_Config.Working_Path
os.chdir("%s" % Working_Path)
from Pre_defined_Variables import Pre_defined_Variables
from AP_FNs import AP_FNs

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 19:16:14 2022

@author: osama
"""


def THC_Class(
    i,
    THC_Class_normal_or_above,
    Lake_O_Stage_AP,
    Lake_O_Schedule_Zone,
    LStgCorres,
    LowChance_Check,
    S77RS_AP,
    S77BS_AP,
    S77RS_Pre_AP_S77_Baseflow,
    Forecast_D_Sal,
    n30d_mavg,
    n30davgForecast,
    LORS08_bf_rel,
    LDS_LC6_1,
    S_O,
    All_4,
    Sabf,
    Swbf,
    Swbu,
    All_4andStage,
    All_4andStagein,
    P_AP_BF_Stg,
    Logic_test_1,
    Post_Ap_Baseflow,
    S77RSplusPreAPS77bsf,
    AndEstNeedsLakeWater,
    AndLowChance61stagelessth11,
    ATHCnora,
    Choose_PAPEWS_1,
    Choose_PAPEWS_2,
    Post_AP_EWS,
    Post_AP_Baseflow_EWS_cfs,
    AdapProt_df,
    Stage_LO,
    Zone_Code,
    df_WSMs,
    Targ_Stg_df,
    S77RS,
    S77BS,
    Estuary_needs_water,
    Choose_1,
    WSM_Zone,
):

    THC_Class_normal_or_above[i] = AP_FNs.THC_Class_normal_or_above(
        AdapProt_df["Tributary Hydrologic Condition"].iloc[i],
        Pre_defined_Variables.THC_threshold,
    )
    # Lake Okeechobee Stage
    Lake_O_Stage_AP[i] = Stage_LO[i + 1]
    # Lake Okeechobee Zone Code
    Lake_O_Schedule_Zone[i] = Zone_Code[i + 1]
    #
    LStgCorres[i] = AP_FNs.LStgCorres(
        AdapProt_df["date"].iloc[i].month,
        df_WSMs["WSM1"].iloc[i + 1],
        Targ_Stg_df["%s%%" % (Pre_defined_Variables.LowChance)].iloc[i],
        Pre_defined_Variables.Opt_LChance_line,
        Pre_defined_Variables.LowChance,
    )
    # Lowchance 6/1 stage falls <11'?
    LowChance_Check[i] = AP_FNs.LowChance_Check(Lake_O_Stage_AP[i], LStgCorres[i])
    # Read LO_Model S77RS
    S77RS_AP[i] = S77RS[i + 2]
    # define Pre-AP S-77 Baseflow
    # FIXME first run only!
    # LO_Model['S77BS'] = np.nan
    # FIXME
    # S77BS = pd.read_csv('./Data/S77BS_Input_%s.csv'%Pre_defined_Variables.Schedule)
    # LO_Model['S77BS'] = S77BS['S77BS']
    S77BS_AP[i] = S77BS[i + 2]
    # Sum S77RS + S77BS
    S77RS_Pre_AP_S77_Baseflow[i] = S77RS_AP[i] + S77BS_AP[i]
    # Forecast daily salinity at Val_I75 if no baseflow or WES(psu), or at Ft. Myers if no baseflow or WES(psu), or at Val_I75  if No S77 contribution to S79.
    if Pre_defined_Variables.OptSalFcast == 1:
        S = "Forecast Daily Salinity at Val_I75 if No Baseflow or EWS (psu)"
    elif Pre_defined_Variables.OptSalFcast == 2:
        S = "Forecast Daily Salinity at Ft. Myers if No Baseflow or EWS (psu)"
    else:
        S = "Forecast Daily Salinity at Val_I75 if No S77 contribution to S79"
    # Option 3 does not use the daily "forecast" salinity from this column (L), nor the 30d ma from Col M.
    # Column N contains the logical T/F pertinent to the AP flowchart.
    # For Option 3 details, see the formula in Col N and corresponding forecast computations in sheet CE_Sal_ValI75.
    Forecast_D_Sal[i] = AP_FNs.Forecast_D_Sal(Pre_defined_Variables.OptSalFcast)
    # Calculate 30-day moving avg salinity (psu)
    n30d_mavg[i] = AP_FNs.n30d_mavg(Pre_defined_Variables.OptSalFcast)
    # Calculate the 30d avg Forecast salinity > the defined CE_SalThreshold psu within 2wks?
    n30davgForecast[i] = AP_FNs.n30davgForecast(
        Estuary_needs_water["Estuary Needs Water?"].iloc[i],
        n30d_mavg[i : i + 13],
        Pre_defined_Variables.OptSalFcast,
        Pre_defined_Variables.CE_SalThreshold,
    )
    # AdapProt_df.to_csv('D:/P_LOOPS/30davgForecastSalgreaterCE_SalThr_cal_%s.csv'%Pre_defined_Variables.Schedule)
    # LORS-08 suggests baseflow release from Lake & estuary needs Lake water
    LORS08_bf_rel[i] = AP_FNs.LORS08_bf_rel(S77BS_AP[i], n30davgForecast[i])
    #
    LDS_LC6_1[i] = AP_FNs.LDS_LC6_1(
        AdapProt_df["Late_Dry_Season"].iloc[i],
        LowChance_Check[i],
        Pre_defined_Variables.Late_Dry_Season_Option,
    )
    # Define Switch at Cell O
    S_O[i] = AP_FNs.S_O(LDS_LC6_1[i], S77BS_AP[i])
    # DEfine All 4 prior conditions are TRUE:
    All_4[i] = AP_FNs.All_4(LORS08_bf_rel[i], LDS_LC6_1[i])
    # Stage above Baseflow SB?
    Sabf[i] = AP_FNs.Sabf(Lake_O_Schedule_Zone[i])
    # Stage within Baseflow SB?
    Swbf[i] = AP_FNs.Swbf(Lake_O_Schedule_Zone[i])
    # Stage within Bene.Use SB?
    Swbu[i] = AP_FNs.Swbu(Lake_O_Schedule_Zone[i])
    # All 4 and Stage > Baseflow SB?
    All_4andStage[i] = AP_FNs.All_4andStage(All_4[i], Sabf[i])
    # All 4 and Stage in Baseflow SB?
    All_4andStagein[i] = AP_FNs.All_4andStagein(All_4[i], Sabf[i])
    # Pre-AP BF>0 AND stg>BF Subband
    P_AP_BF_Stg[i] = AP_FNs.P_AP_BF_Stg(Lake_O_Schedule_Zone[i], S77BS_AP[i])
    # Post-AP Baseflow (cfs)
    # Modified formula on 12/7/2021 to allow testing alternative baseflow scenarios.
    # Changed from:
    # =IF(V11,J11,IF(W11,MIN(J11,450),0))
    # to:
    # =IF(V11,J11,IF(W11,MIN(J11,CHOOSE(Opt_AdapProt,450,ActiveSchedule!$G$11)),0))
    # Create a logic test to be used for Post-AP Baseflow (cfs)
    Logic_test_1[i] = AP_FNs.Logic_test_1(
        All_4andStage[i], P_AP_BF_Stg[i], Pre_defined_Variables.Opt_NoAP_above_BF_SB
    )
    # Main Function
    Post_Ap_Baseflow[i] = AP_FNs.Post_Ap_Baseflow(
        Logic_test_1[i], S77BS_AP[i], All_4andStagein[i], Choose_1
    )
    # S77RS+PreAPS77bsf=0 and [Stage above LOWSM]?
    # New logic added July 2021 to test restricted delivery of environmental water supply to Caloosahatchee Estuary when Lake O stage is below the WST line (ie, within the LOWSM band).
    # Opt_CEews_LOWSM=0, same logic as original AP.  Test if stage above LOWSM.
    # =(AND(K11=0,F11>1))
    # Opt_CEews_LOWSM<>0, new logic allows Env WS releases even if stage is in LOWSM.
    # For the logic in this column, formulas were changed from:
    # =(AND(K11=0,F11>1))
    # TO
    # =IF(Opt_CEews_LOWSM=0,AND(K11=0,F11>1)),(K11=0))
    # This allows Env WS releases for any stage, but logic in subsequent columns cuts back the ews release based on the input cutback percentages that apply to the target CE env ws release.
    # See column "Post-AP EWS" comment and formulas in Col AD.
    S77RSplusPreAPS77bsf[i] = AP_FNs.S77RSplusPreAPS77bsf(
        S77RS_Pre_AP_S77_Baseflow[i],
        Lake_O_Schedule_Zone[i],
        Pre_defined_Variables.Opt_CEews_LOWSM,
    )
    # AND Est Needs Lake Water?
    AndEstNeedsLakeWater[i] = AP_FNs.AndEstNeedsLakeWater(
        n30davgForecast[i], S77RSplusPreAPS77bsf[i]
    )
    # AND Low chance 6/1 stage <11'?
    AndLowChance61stagelessth11[i] = AP_FNs.AndLowChance61stagelessth11(
        LDS_LC6_1[i], AndEstNeedsLakeWater[i]
    )
    # AND THC normal or above?
    ATHCnora[i] = AP_FNs.ATHCnora(
        AndLowChance61stagelessth11[i],
        THC_Class_normal_or_above[i],
        AdapProt_df["Late_Dry_Season"].iloc[i],
        Pre_defined_Variables.Opt_THCbypLateDS,
    )
    # Post-AP EWS (cfs)
    # Define Choose_PAPEWS_1 and 2
    Choose_PAPEWS_1[i] = AP_FNs.Choose_PAPEWS_1(
        WSM_Zone[i + 2],
        Pre_defined_Variables.APCB1,
        Pre_defined_Variables.APCB2,
        Pre_defined_Variables.APCB3,
        Pre_defined_Variables.APCB4,
    )
    #
    Choose_PAPEWS_2[i] = AP_FNs.Choose_PAPEWS_2(
        Pre_defined_Variables.Opt_CEews_LOWSM, Pre_defined_Variables.CalEst_ews
    )
    #
    Post_AP_EWS[i] = AP_FNs.Post_AP_EWS(
        ATHCnora[i],
        WSM_Zone[i + 2],
        Choose_PAPEWS_1[i],
        Choose_PAPEWS_2[i],
        Pre_defined_Variables.CalEst_ews,
    )
    # Post-AP Baseflow + EWS (cfs)
    Post_AP_Baseflow_EWS_cfs[i] = Post_Ap_Baseflow[i] + Post_AP_EWS[i]
    THC_Out = {}
    THC_Out["Post_AP_EWS"] = Post_AP_EWS[i]
    THC_Out["Post_Ap_Baseflow"] = Post_Ap_Baseflow[i]
    return THC_Out
