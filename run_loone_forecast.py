from loone_data_prep.utils import photo_period, get_synthetic_data, wind_induced_waves
from loone_data_prep.forecast_scripts import (
    predict_PI,
    trib_cond,
    forecast_stages,
    get_Chla_predicted,
    get_NO_Loads_predicted,
    Chla_merged,
    loone_q_predict,
    loone_wq_predict,
    new_combined_weather_forecast
)
from loone_data_prep import utils
from loone import LOONE_Q
from loone import LOONE_NUT
from loone import LOONE_WQ
import os
import pandas as pd
import datetime
import numpy as np
import shutil
import glob
from loone_data_prep import (
    water_level_data,
    water_quality_data,
    weather_data,
    flow_data,
    utils,
    LOONE_DATA_PREP,
    GEOGLOWS_LOONE_DATA_PREP,
)

def _get_ts_data(input_dir, output_dir, cache_path, temp_dir):
    """
    Downloads the ts data, prepares it for LOONE, and puts the output at the path specified by output_dir.

    Args:
        input_dir (str): A path to the directory that holds the input files used to create the output files.
        output_dir (str): A path to the directory where the generated output files should go.
        cache_path (str): The path to the cache directory which holds the dbhydro cache directory named "dbhydro_cache".
        temp_dir (str): A path to the directory that will hold the files that are only needed temporarily.
    """
    # Create cache if it doesn't exist
    dbhydro_cache_path = os.path.join(cache_path, "dbhydro_cache")

    if not os.path.exists(dbhydro_cache_path):
        # Make the cache directory for the dbhydro data
        os.makedirs(dbhydro_cache_path)

    # Water Level Data
    water_level_status = water_level_data.get_all.main(dbhydro_cache_path)

    # Water Quality Data
    water_quality_inflows_status = water_quality_data.get_inflows.main(
        dbhydro_cache_path
    )
    water_quality_lake_wq_status = water_quality_data.get_lake_wq.main(
        dbhydro_cache_path
    )

    # Weather Data
    weather_data_status = weather_data.get_all.main(dbhydro_cache_path)

    # Forecast historical flow data
    inflows_status = flow_data.get_inflows.main(dbhydro_cache_path)
    outflows_status = flow_data.get_outflows.main(dbhydro_cache_path)

    # PI.csv
    try:
        print("Downloading PI.csv")
        utils.get_pi(input_dir)  # PI should not be cached (new value each week)
    except Exception as e:
        print(f"Error downloading PI.csv: {e}")

    # Output Download Failures
    if "error" in water_level_status:
        print(water_level_status["error"])

    if "error" in water_quality_inflows_status:
        print(water_quality_inflows_status["error"])

    if "error" in water_quality_lake_wq_status:
        print(water_quality_lake_wq_status["error"])

    if "error" in weather_data_status:
        print(weather_data_status["error"])

    if "error" in inflows_status:
        print(inflows_status["error"])

    if "error" in outflows_status:
        print(outflows_status["error"])

    # Copy cached files to input_dir
    cached_files = glob.glob(os.path.join(dbhydro_cache_path, "*"))
    for file_path in cached_files:
        file_name = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(input_dir, file_name))

    # Interpolate the data
    utils.interpolate_all(input_dir)

    # Prepare the data for LOONE
    LOONE_DATA_PREP.main(input_dir, output_dir)

    # Get WindShearStress.csv and Current_ShearStress.csv
    utils.wind_induced_waves(
        input_dir, output_dir, "LOWS.csv", "Average_LO_Storage_3MLag.csv"
    )

    # Get nu.csv
    utils.kinematic_viscosity(output_dir, "Filled_WaterT.csv")
    
def get_geoglows_ts_data(input_dir, output_dir, cache_path, observed_geoglows_data_dir):
    """
    Downloads the geoglows data, prepares it for LOONE, and puts the output at the path specified by output_dir.

    Args:
        input_dir (tempfile.TemporaryDirectory): A temporary directory that holds the input files used to create the output files.
        output_dir (str): A path to the directory where the generated output files should go.
        cache_path (str): The path to the cache directory which holds the geoglows cache directory named "geoglows_cache".
        observed_geoglows_data_dir (str): A path to the directory that holds the observed geoglows data. Only necessary when bias correcting the forecast flows.
    """
    # Get GEOGloWS data
    flow_data.get_forecast_flows.main(
        workspace=input_dir,
        bias_corrected=True,
        observed_data_dir=input_dir,
        cache_path=cache_path,
    )

    # Run nutrient prediction on the data for phosphate
    utils.nutrient_prediction(
        input_dir=input_dir,
        output_dir=output_dir,
        constants=utils.DEFAULT_EXPFUNC_PHOSPHATE_CONSTANTS,
        nutrient="PHOSPHATE",
    )

    # Run nutrient prediction on the data for nitrogen
    utils.nutrient_prediction(
        input_dir=input_dir,
        output_dir=output_dir,
        constants=utils.DEFAULT_EXPFUNC_NITROGEN_CONSTANTS,
        nutrient="NITROGEN",
    )

    for i in range(1, 52):
        GEOGLOWS_LOONE_DATA_PREP.main(input_dir, output_dir, f"{i:02d}")
        if not os.path.exists(os.path.join(input_dir, "LOWS_predicted.csv")):
                shutil.copyfile(os.path.join(output_dir, "LOWS_predicted.csv"), os.path.join(input_dir, "LOWS_predicted.csv"))
        if not os.path.exists(os.path.join(input_dir, f"Netflows_acft_geoglows_{i:02d}.csv")):
                shutil.copyfile(os.path.join(output_dir, f"Netflows_acft_geoglows_{i:02d}.csv"), os.path.join(input_dir, f"Netflows_acft_geoglows_{i:02d}.csv"))
        if not os.path.exists(os.path.join(input_dir, f"Basin_RO_inputs_{i:02d}.csv")):
                shutil.copyfile(os.path.join(output_dir, f"Basin_RO_inputs_{i:02d}.csv"), os.path.join(input_dir, f"Basin_RO_inputs_{i:02d}.csv"))
                
    utils.kinematic_viscosity(output_dir, "Filled_WaterT_predicted.csv", "nu_predicted.csv")


# Update this file path
file_collection = "/home/rhuber/development/LOONE_CLEAN/data"
temp = os.path.join(file_collection, "temp")

#This is getting the data from dbhydro
_get_ts_data(file_collection, file_collection, file_collection, temp)

#These are being run in historical mode. This is optional and could be commented out
LOONE_Q(file_collection)
# LOONE_NUT(file_collection)

Q_in = pd.read_csv(os.path.join(file_collection, 'LO_Inflows_BK.csv'))
photo_period(file_collection, doy=np.arange(1, len(Q_in)))

#Get needed forecast data
extended_pi_path = os.path.join(file_collection, 'extended_PI.csv')
forecast_weather_data_path = os.path.join(file_collection, 'forecasted_weather_data.csv')
pi_path = os.path.join(file_collection, 'PI.csv')
predict_PI.extend_PI(pi_path, extended_pi_path)

# Get weather forecast data - comment out this section if it has run already this day because it can be slow
forecast_weather_data_path = os.path.join(file_collection, 'forecasted_weather_data.csv')
new_combined_weather_forecast.generate_all_outputs(file_collection)

# Get the GEOGLOWS RFS data, this line will take a while, so if it has already been run for the day, it can be commented out
get_geoglows_ts_data(file_collection, file_collection, "cache_path", file_collection)

for i in range(1, 52):
    trib_cond.create_trib_cond(
                    forecast_weather_data_path,
                    f"{file_collection}/Netflows_acft_geoglows_{i:02d}.csv",
                    f"{file_collection}/750072741_INFLOW_cmd_geoglows.csv",
                    extended_pi_path,
                    f"{file_collection}/Trib_cond_predicted_{i:02d}.csv",
                    i)
forecast_stages.forecast_stages(file_collection)

# This is where the rest of necessary input files are generated using historical averages
loone_q_predict.generate_historical_predictions(file_collection)

# This runs in a loop because must be run for each ensemble member
for i in range(1, 52):
#     #loone q should be mostly in cubic feet, the outputs should be in cubic feet
    LOONE_Q(file_collection, forecast=True, ensemble = i)

    # Get the wind and current shear stress from outputs of loone_q
    wind_induced_waves(
        file_collection, 
        file_collection, 
        "LOWS_predicted.csv", 
        f"LOONE_Q_Outputs_{i:02d}.csv", 
        wind_shear_stress_out=f"WindShearStress_{i:02d}.csv", 
        current_shear_stress_out=f"Current_ShearStress_{i:02d}.csv", 
        forecast=True
    )
    
for i in range(1, 52):
    dst_file_path = os.path.join(file_collection, f'LOONE_Nut_Output_ens{i:02d}.csv')
    loads_external_filename = f'LO_External_Loadings_3MLag_{i:02d}.csv'
    flow_df_filename = f'geoglows_flow_df_ens_{i:02d}_predicted.csv'
    loone_q_path = os.path.join(file_collection, f'LOONE_Q_Outputs_{i:02d}.csv')

    LOONE_NUT(
        file_collection,
        dst_file_path,
        loads_external_filename,
        flow_df_filename,
        loone_q_path,
        file_collection,
        forecast_mode=True,
        ensemble = i
    )
    print("LOONE_NUT finished")
    
# This is running in historical mode
LOONE_WQ(file_collection)

Q_in = pd.read_csv(os.path.join(file_collection, 'LO_Inflows_BK_forecast_01.csv'))
#TODO - not sure if this is actually needed with a forecast version, but keeping it here for now but it may be repetitive
photo_period(file_collection, file_name='PhotoPeriod_forecast')
datetime_str = Q_in['date'].iloc[0]
date_start = datetime.datetime.strptime(datetime_str, '%Y-%m-%d')

S65E_NO_data = pd.read_csv(os.path.join(file_collection, 'water_quality_S65E_NITRATE+NITRITE-N_Interpolated.csv')) # mg/m3
S65E_Chla_data = pd.read_csv(os.path.join(file_collection, 'S65E_Chla_Merged.csv')) # mg/m3
if datetime_str not in S65E_NO_data['date'].values:
    S65E_NO_data = get_synthetic_data(date_start, S65E_NO_data)
    S65E_NO_data.to_csv(os.path.join(file_collection, 'water_quality_S65E_NITRATE+NITRITE-N_Interpolated_forecast.csv'), index=False) # mg/m3
if datetime_str not in S65E_Chla_data['date'].values:
    S65E_Chla_data = get_synthetic_data(date_start, S65E_Chla_data)
# TODO: Do we want to forecast this based on ensembles? Or just one overall guess? Like how should we be going about getting the forecast?
    S65E_Chla_data.to_csv(os.path.join(file_collection, 'S65E_Chla_Merged_forecast.csv'), index=False) # mg/m3
get_Chla_predicted.get_Chla_predicted(file_collection, file_collection)
get_NO_Loads_predicted.get_NO_Loads_predicted(file_collection, file_collection)
Chla_merged.loads_predicted(file_collection, file_collection)
loone_wq_predict.create_forecasts(file_collection)
for i in range(1, 52):
    LOONE_WQ(file_collection, 'PhotoPeriod_forecast', forecast_mode=True, ensemble_number = i)