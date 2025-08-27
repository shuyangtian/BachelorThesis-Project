import numpy as np
import pandas
import os, sys
import matplotlib.pyplot as plt

from global_constants import _PATHS, _LISTS

def print_ids():
    print("\npatient_id list: ")
    print(_LISTS.shimmer_patient_list)
    print("\nday_id list: ")
    print(_LISTS.day_list)
    print("\nsensor_id list: ")
    print(_LISTS.shimmer_locations)

def get_full_patient_imu_path(patient_id, day_id, sensor_id, is_loc_boston=True):
    if is_loc_boston:
        patient_id_string = f'patient{patient_id}'
    else:
        patient_id_string = f'patient{patient_id}_NY'
    return os.path.join(_PATHS.root, 
                        "SENSOR",
                        sensor_id, 
                        patient_id_string, 
                        f'rawData_Day{day_id}.txt')

def get_table_path(table_file_path):
    return os.path.join(_PATHS.root, "SENSOR", "TABLES", table_file_path)

def read_raw_data(patient_id, day_id, sensor_id, is_loc_boston=True, delimiter='\t'):
    filename = get_full_patient_imu_path(
        patient_id=patient_id,
        day_id=day_id,
        sensor_id=sensor_id,
        is_loc_boston=is_loc_boston
    )
    return pandas.read_csv(filename, delimiter=delimiter)

def read_table(table_file_path, delimiter=','):
    filename = get_table_path(table_file_path=table_file_path)
    return pandas.read_csv(filename, delimiter=delimiter)

def get_raw_shimmer_data_for_patient(patient_id, display_frames = False):
    """
    The Labelled data (in tbl_task_sc_2.csv) corresponds to day 1 and day 4 of the raw data.
    :param patient_id - patient or subject ID
    :param display_frames - whether to display the dataframes in a formatted manner or not TODO: FIXME
    """
    df1b = read_raw_data(
        patient_id=patient_id, 
        day_id='1', 
        sensor_id='Shimmer_Back'
    )
    df4b = read_raw_data(
        patient_id=patient_id, 
        day_id='4', 
        sensor_id='Shimmer_Back'
    )
    dfb = pandas.concat([df1b, df4b])

    df1la = read_raw_data(
        patient_id=patient_id, 
        day_id='1', 
        sensor_id='Shimmer_LeftAnkle'
    )
    df4la = read_raw_data(
        patient_id=patient_id, 
        day_id='4', 
        sensor_id='Shimmer_LeftAnkle'
    )
    dfla = pandas.concat([df1la, df4la])
    dfla_cols = dfla.columns.difference(dfb.columns)

    df1ra = read_raw_data(
        patient_id=patient_id, 
        day_id='1', 
        sensor_id='Shimmer_RightAnkle'
    )
    df4ra = read_raw_data(
        patient_id=patient_id, 
        day_id='4', 
        sensor_id='Shimmer_RightAnkle'
    )
    dfra = pandas.concat([df1ra, df4ra])
    dfra_cols = dfra.columns.difference(dfb.columns)

    df1lw = read_raw_data(
        patient_id=patient_id, 
        day_id='1', 
        sensor_id='Shimmer_LeftWrist'
    )
    df4lw = read_raw_data(
        patient_id=patient_id, 
        day_id='4', 
        sensor_id='Shimmer_LeftWrist'
    )
    dflw = pandas.concat([df1lw, df4lw])
    dflw_cols = dflw.columns.difference(dfb.columns)

    df1rw = read_raw_data(
        patient_id=patient_id, 
        day_id='1', 
        sensor_id='Shimmer_RightWrist'
    )
    df4rw = read_raw_data(
        patient_id=patient_id, 
        day_id='4', 
        sensor_id='Shimmer_RightWrist'
    )
    dfrw = pandas.concat([df1rw, df4rw])
    dfrw_cols = dfrw.columns.difference(dfb.columns)

    df = pandas.concat([dfb, dfla[dfla_cols], dfra[dfra_cols], dflw[dflw_cols], dfrw[dfrw_cols]], axis=1)
    if display_frames:
        display(df)
    return df
