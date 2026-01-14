import os
from yaml import safe_load
import pandas as pd
import numpy as np


def load_config(workspace: str) -> dict:
    """Load the configuration file.

    Args:
        workspace (str): Path to directory containing the config file and its associated input data.

    Returns:
        dict: dictionary containing the configuration parameters.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """
    for config_file_name in ["config.yaml", "config.yml"]:
        config_file = os.path.join(workspace, config_file_name)
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = safe_load(f)
            return config
    else:
        raise FileNotFoundError("Config file not found in the workspace.")


def leap_year(year: int) -> bool:
    """Determines if a given year is a leap year.

    A leap year is exactly divisible by 4 except for century years (years ending with 00).
    The century year is a leap year only if it is perfectly divisible by 400.

    Args:
        year (int): The year to check.

    Returns:
        bool: True if the year is a leap year, False otherwise.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def replicate(
    year: int, day_num: int, x: int, targ_stg: dict
) -> float:  # Where x is the percentage value (i.e., 10,20,30,40,50,60)
    """Retrieves the value from the target stage DataFrame corresponding to the given day and percentage.
    Takes leap years into account.

    Args:
        year (int): The year that day_num is in.
        day_num (int): The day number to get the value for (ranging from 0 to 365).
        x (int): The percentage value (i.e., 10, 20, 30, 40, 50, 60).
        targ_stg (pandas.DataFrame): The target stage DataFrame.

    Returns:
        float: The value from the target stage DataFrame corresponding to the day number and the given percentage.
    """
    leap_day_val = targ_stg[f"{x}%"].iloc[59]
    if leap_year(year):
        day_num_adj = day_num
    else:
        day_num_adj = day_num + (1 if day_num >= 60 else 0)
    day_value = (
        leap_day_val
        if day_num_adj == 60 and leap_year(year)
        else targ_stg[f"{x}%"].iloc[day_num_adj - 1]
    )
    return day_value

def correct_month(df, month, date_col="date"):
    """
    Correct year rollover for any datetime data based on a cutoff month.
    Does not change the original weekday.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    ref_year = df[date_col].dt.year.min()
    mask = (df[date_col].dt.year == ref_year) & (df[date_col].dt.month < month)
    
    # Shift years
    df.loc[mask, date_col] += pd.DateOffset(years=1)
    
    df = df.drop_duplicates(subset=date_col)

    return df.sort_values(date_col).reset_index(drop=True)

def correct_month_with_padding(
    df: pd.DataFrame,
    month,
    date_col: str = "date",
) -> pd.DataFrame:
    """
    Runs the correct_month function, but also prepends two days prior to the first date after correction.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe to change start date for
        Month it should be initialized in
    date_col : str, default "date"
        Name of the date column

    Returns
    -------
    pd.DataFrame
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    jan1_dates = df.loc[
        (df[date_col].dt.month == 1) & (df[date_col].dt.day == 1),
        date_col
    ]

    if jan1_dates.empty:
        raise ValueError("No January 1 found in dataframe")

    start_date = jan1_dates.min()

    # Drop everything before that January 1
    df = df[df[date_col] >= start_date].reset_index(drop=True)

    df = correct_month(df, month)

    # Prepend exactly two previous days
    first_date = df[date_col].iloc[0]

    pad_df = pd.DataFrame({
        date_col: [
            first_date - pd.Timedelta(days=2),
            first_date - pd.Timedelta(days=1),
        ]
    })

    # Add all other columns as NaN
    for col in df.columns:
        if col != date_col:
            pad_df[col] = 0 # TODO should this be NaN?

    df = df.drop_duplicates(subset="date")
    
    df = (
        pd.concat([pad_df, df], ignore_index=True)
          .sort_values(date_col)
          .reset_index(drop=True)
    )

    return df


def daily_average_calc(df: pd.DataFrame, value_cols: list, placeholder_year: int = 2020) -> pd.DataFrame:
    """
    Compute daily averages for one or more columns across years, returning
    a DataFrame with a 'date' column (placeholder year) and average values.
    Column names are kept the same.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a 'date' column and one or more numeric columns.
    value_cols : list of str
        Names of columns to compute daily averages for.
    placeholder_year : int
        Year to use for the output 'date' column (default: 2020, leap year).
        
    Returns
    -------
    pd.DataFrame
        DataFrame with 'date' and averaged columns, keeping original names.
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_year'] = df['date'].dt.dayofyear
    
    # Group by day-of-year and compute mean for each specified column
    daily_avg = df.groupby('day_of_year', as_index=False)[value_cols].mean()
    
    daily_avg['date'] = pd.to_datetime(
        daily_avg['day_of_year'] - 1,  # zero-based offset
        unit='D',
        origin=pd.Timestamp(f'{placeholder_year}-01-01')
    )
    
    # Reorder columns: date first, then the value columns
    daily_avg = daily_avg[['date'] + value_cols]
    
    return daily_avg



