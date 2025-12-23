# This Script Interpolates each Water Shortage Management (WSMs) and each Regulation Schedule Breakpoint Zone (D, C, B, and A).
from calendar import monthrange
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy import interpolate
from loone.data import Data as DClass
from loone.utils import load_config


def WSMs(workspace: str, forecast: bool = False, ensemble: int = None, month=None) -> None:
    """Generate WSMs (Weather State Modifiers) based on the given workspace."""

    os.chdir(workspace)

    config = load_config(workspace)
    data = DClass(workspace, forecast, ensemble, month)

    # --- Date handling ---
    if forecast:
        today = datetime.today().date()
        start_date = today
        end_date = today + timedelta(days=16)
    else:
        sy, sm, sd = map(int, config["start_date_entry"])
        ey, em, ed = map(int, config["end_date_entry"])
        start_date = datetime(sy, sm, sd).date()
        end_date = datetime(ey, em, ed).date() + timedelta(days=1)
        
    if config["sim_type"] == 3 and month:
        start_date = datetime(start_date.year, month, 1).date()
        end_date = datetime(
            start_date.year + 1,
            month-1,
            monthrange(start_date.year, month-1)[1],
        ).date()+ timedelta(days=1)

    # Build daily date range
    df_wsms = pd.DataFrame(pd.date_range(start=start_date, end=end_date, freq="D"),
                           columns=["date"])

    wsm_length = len(df_wsms)
    op_zones = [z for z in data.WSMs_RSBKs.columns if z not in ("Date", "Day")]

    # Convert dates to day-of-year integers for interpolation
    doy = df_wsms["date"].dt.strftime("%j").astype(int)

    # --- Vectorized interpolation for all WSM columns ---
    for col in op_zones:
        interp_func = interpolate.interp1d(
            data.WSMs_RSBKs["Day"],
            data.WSMs_RSBKs[col],
            kind="linear",
            fill_value="extrapolate"
        )
        df_wsms[col] = interp_func(doy)

    # Add Count column
    df_wsms["count"] = doy

    # --- New Tree / No New Tree switch ---
    df_wsms["C-b"] = (
        data.WSMs_RSBKs["C-b_NewTree"]
        if config["opt_new_tree"] == 1
        else data.WSMs_RSBKs["C-b_NoNewTree"]
    )

    # Remove unused columns if they exist
    df_wsms = df_wsms.drop(columns=[c for c in ["C-b_NewTree", "C-b_NoNewTree"]
                                    if c in df_wsms.columns], errors="ignore")

    # --- Add correct previous-day row using interpolation ---
    prev_date = df_wsms.loc[0, "date"] - pd.Timedelta(days=1)
    prev_doy = int(prev_date.strftime("%j"))

    # Build row with EXACT same columns as df_wsms
    prev_vals = {}

    for col in df_wsms.columns:
        if col == "date":
            prev_vals[col] = prev_date

        elif col == "count":
            prev_vals[col] = prev_doy

        # Columns that require interpolation from WSMs_RSBKs
        elif col in data.WSMs_RSBKs.columns:
            interp_func = interpolate.interp1d(
                data.WSMs_RSBKs["Day"],
                data.WSMs_RSBKs[col],
                kind="linear",
                fill_value="extrapolate",
            )
            prev_vals[col] = float(interp_func(prev_doy))

        # Special case: C-b because it's split into NewTree/NoNewTree in source
        elif col == "C-b":
            cb_source = (
                data.WSMs_RSBKs["C-b_NewTree"]
                if config["opt_new_tree"] == 1
                else data.WSMs_RSBKs["C-b_NoNewTree"]
            )
            cb_interp = interpolate.interp1d(
                data.WSMs_RSBKs["Day"],
                cb_source,
                kind="linear",
                fill_value="extrapolate",
            )
            prev_vals[col] = float(cb_interp(prev_doy))

        else:
            # Any other column not related to interpolation: copy first value
            prev_vals[col] = df_wsms[col].iloc[0]

    # Insert row at the top
    prev_row_df = pd.DataFrame([prev_vals])
    df_wsms = pd.concat([prev_row_df, df_wsms], ignore_index=True)


    df_wsms.to_csv("df_WSMs.csv", index=False)


