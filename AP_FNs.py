# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:57:27 2020

@author: osama
"""


class AP_FNs:
    def THC_Class_normal_or_above(
        Tributary_Hydrologic_Condition, Pre_defined_Variables_THC_threshold
    ):
        if Tributary_Hydrologic_Condition > Pre_defined_Variables_THC_threshold:
            THC_Class = True
        else:
            THC_Class = False
        return THC_Class

    def LStgCorres(
        month,
        WSMs_WSM1,
        Targ_Stg_df_Pre_defined_Variables_LowChance,
        Pre_defined_Variables_Opt_LChance_line,
        Pre_defined_Variables_LowChance,
    ):
        if Pre_defined_Variables_Opt_LChance_line == 1:
            if month > 5 and month < 10:
                St = WSMs_WSM1
            else:
                St = WSMs_WSM1 + 0.5
        elif Pre_defined_Variables_LowChance == 1 or (month > 5 and month < 10):
            St = -999
        else:
            St = Targ_Stg_df_Pre_defined_Variables_LowChance
        return St

    def LowChance_Check(Lake_O_Stage_AP, LStgCorres):
        if Lake_O_Stage_AP > LStgCorres:
            Ch = True
        else:
            Ch = False
        return Ch

    def Forecast_D_Sal(Pre_defined_Variables_OptSalFcast):
        import numpy as np

        if Pre_defined_Variables_OptSalFcast == 1:
            pass
        elif Pre_defined_Variables_OptSalFcast == 2:
            pass
        elif Pre_defined_Variables_OptSalFcast == 3:
            F = np.nan
        return F

    def n30d_mavg(Pre_defined_Variables_OptSalFcast):
        import numpy as np

        if Pre_defined_Variables_OptSalFcast == 1:
            pass
        elif Pre_defined_Variables_OptSalFcast == 2:
            pass
        elif Pre_defined_Variables_OptSalFcast == 3:
            F = np.nan
        return F

    def n30davgForecast(
        Estuary_needs_water,
        n30d_mavg_i2iplus13,
        Pre_defined_Variables_OptSalFcast,
        Pre_defined_Variables_CE_SalThreshold,
    ):
        if Pre_defined_Variables_OptSalFcast == 3:
            Est = Estuary_needs_water
        elif max(n30d_mavg_i2iplus13) > Pre_defined_Variables_CE_SalThreshold:
            Est = True
        else:
            Est = False
        return Est

    def LORS08_bf_rel(S77BS_AP, n30davgForecast):
        if S77BS_AP > 0:
            L = n30davgForecast
        else:
            L = False
        return L

    def LDS_LC6_1(
        Late_Dry_Season, LowChance_Check, Pre_defined_Variables_Late_Dry_Season_Option
    ):
        if Pre_defined_Variables_Late_Dry_Season_Option == 1:
            if Late_Dry_Season == True:
                LD = LowChance_Check
            else:
                LD = False
        else:
            LD = LowChance_Check
        return LD

    def S_O(LDS_LC6_1, S77BS_AP):
        if LDS_LC6_1 == False:
            if S77BS_AP > 0:
                S = 1
            else:
                S = 0
        else:
            S = 0
        return S

    def All_4(LORS08_bf_rel, LDS_LC6_1):
        if LORS08_bf_rel == True:
            All = LDS_LC6_1
        else:
            All = False
        return All

    def Sabf(Lake_O_Schedule_Zone):
        if Lake_O_Schedule_Zone > 3:
            Sa = True
        else:
            Sa = False
        return Sa

    def Swbf(Lake_O_Schedule_Zone):
        if Lake_O_Schedule_Zone == 3:
            Sw = True
        else:
            Sw = False
        return Sw

    def Swbu(Lake_O_Schedule_Zone):
        if Lake_O_Schedule_Zone == 2:
            Swb = True
        else:
            Swb = False
        return Swb

    def All_4andStage(All_4, Sabf):
        if All_4 == True and Sabf == True:
            AAA = True
        else:
            AAA = False
        return AAA

    def All_4andStagein(All_4, Sabf):
        if All_4 == True and Sabf == False:
            AAA = True
        else:
            AAA = False
        return AAA

    def P_AP_BF_Stg(Lake_O_Schedule_Zone, S77BS_AP):
        if (Lake_O_Schedule_Zone > 3 and Lake_O_Schedule_Zone < 7) and S77BS_AP > 0:
            P = True
        else:
            P = False
        return P

    def Logic_test_1(
        All_4andStage, P_AP_BF_Stg, Pre_defined_Variables_Opt_NoAP_above_BF_SB
    ):
        if Pre_defined_Variables_Opt_NoAP_above_BF_SB == 0:
            Logic = All_4andStage
        else:
            Logic = P_AP_BF_Stg
        return Logic

    def Post_Ap_Baseflow(Logic_test_1, S77BS_AP, All_4andStagein, Choose_1):
        if Logic_test_1 == True:
            PB = S77BS_AP
        elif All_4andStagein == True:
            PB = min(S77BS_AP, Choose_1)
        else:
            PB = 0
        return PB

    def S77RSplusPreAPS77bsf(
        S77RS_Pre_AP_S77_Baseflow,
        Lake_O_Schedule_Zone,
        Pre_defined_Variables_Opt_CEews_LOWSM,
    ):
        if Pre_defined_Variables_Opt_CEews_LOWSM == 0:
            if S77RS_Pre_AP_S77_Baseflow == 0 and Lake_O_Schedule_Zone > 1:
                S77RSPAPS77bsf = True
            else:
                S77RSPAPS77bsf = False
        elif S77RS_Pre_AP_S77_Baseflow == 0:
            S77RSPAPS77bsf = True
        else:
            S77RSPAPS77bsf = False
        return S77RSPAPS77bsf

    def AndEstNeedsLakeWater(n30davgForecast, S77RSplusPreAPS77bsf):
        if n30davgForecast == True and S77RSplusPreAPS77bsf == True:
            AENLW = True
        else:
            AENLW = False
        return AENLW

    def AndLowChance61stagelessth11(LDS_LC6_1, AndEstNeedsLakeWater):
        if LDS_LC6_1 == True and AndEstNeedsLakeWater == True:
            ALC = True
        else:
            ALC = False
        return ALC

    def ATHCnora(
        AndLowChance61stagelessth11,
        THC_Class_normal_or_above,
        Late_Dry_Season,
        Pre_defined_Variables_Opt_THCbypLateDS,
    ):
        if Pre_defined_Variables_Opt_THCbypLateDS == 1:
            if AndLowChance61stagelessth11 == True and (
                THC_Class_normal_or_above == True or Late_Dry_Season == True
            ):
                AT = True
            else:
                AT = False
        else:
            if (
                AndLowChance61stagelessth11 == True
                and THC_Class_normal_or_above == True
            ):
                AT = True
            else:
                AT = False
        return AT

    def Choose_PAPEWS_1(
        WSM_Zone,
        Pre_defined_Variables_APCB1,
        Pre_defined_Variables_APCB2,
        Pre_defined_Variables_APCB3,
        Pre_defined_Variables_APCB4,
    ):
        if WSM_Zone == 1:
            C1 = Pre_defined_Variables_APCB1 / 100
        elif WSM_Zone == 2:
            C1 = Pre_defined_Variables_APCB2 / 100
        elif WSM_Zone == 3:
            C1 = Pre_defined_Variables_APCB3 / 100
        elif WSM_Zone == 4:
            C1 = Pre_defined_Variables_APCB4 / 100
        else:
            C1 = -9999
        return C1

    def Choose_PAPEWS_2(
        Pre_defined_Variables_Opt_CEews_LOWSM, Pre_defined_Variables_CalEst_ews
    ):
        if Pre_defined_Variables_Opt_CEews_LOWSM + 1 == 1:
            C2 = 0
        elif Pre_defined_Variables_Opt_CEews_LOWSM + 1 == 2:
            C2 = Pre_defined_Variables_CalEst_ews
        elif Pre_defined_Variables_Opt_CEews_LOWSM + 1 == 3:
            C2 = 300
        return C2

    def Post_AP_EWS(
        ATHCnora,
        WSM_Zone,
        Choose_PAPEWS_1,
        Choose_PAPEWS_2,
        Pre_defined_Variables_CalEst_ews,
    ):
        if ATHCnora == True:
            if WSM_Zone == 0:
                PAEW = Pre_defined_Variables_CalEst_ews
            else:
                PAEW = (1 - Choose_PAPEWS_1) * Choose_PAPEWS_2
        else:
            PAEW = 0
        return PAEW
