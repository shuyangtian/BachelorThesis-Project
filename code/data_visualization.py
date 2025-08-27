import numpy as np
import pandas
import os, sys
import matplotlib.pyplot as plt

from global_constants import _PATHS, _LISTS
from data_loading import *

def plot_task_tbl_time_stats(is_shimmer=True, secondary_col='score'):
    """
    This function plots the time spent stats for the phenotypes (tremor, bradykinesia, dyskinesia) 
    in the shimmer table - tbl_task_sc_2.csv grouped by values in the secondary column
    :param secondary_col - The secondary column 
    """
    
    if is_shimmer:
        table_file_path =_PATHS.shimmer_task_tbl_path
    else:
        table_file_path = _PATHS.smartdevice_task_tbl_path

    tbl = pandas.read_csv(get_table_path(table_file_path=table_file_path), delimiter=',')
    
    phenotype_list = tbl['phenotype'].unique()
    print(phenotype_list)

    tbl_group_by_ph = {}
    time_group_by_ph = {}

    time_group_by_ph_and_col = {}
    for i, ph in enumerate(phenotype_list):
        tbl_group_by_ph[ph] = tbl[np.logical_and(
                                    tbl['phenotype'] == ph, 
                                    True,
                                    # tbl['body_segment']=='RightUpperLimb'
                                )]
        time_group_by_ph[ph] = np.sum(tbl_group_by_ph[ph]['timestamp_end'] - tbl_group_by_ph[ph]['timestamp_start'])
        # print(time_group_by_ph)
        time_group_by_ph_and_col[ph] = {key:0 for key in tbl_group_by_ph[ph][secondary_col].unique()}
        for key in time_group_by_ph_and_col[ph]:
            sub_tbl = tbl_group_by_ph[ph][tbl_group_by_ph[ph][secondary_col] == key]
            time_group_by_ph_and_col[ph][key] = 100 * (np.sum(sub_tbl['timestamp_end'] - sub_tbl['timestamp_start'])/time_group_by_ph[ph])

        time_group_by_ph_and_col[ph] = {key:time_group_by_ph_and_col[ph][key] for key in sorted(time_group_by_ph_and_col[ph])}
        if 'NotApplicable' in time_group_by_ph_and_col[ph]:
            time_group_by_ph_and_col[ph]['NA'] = time_group_by_ph_and_col[ph].pop('NotApplicable')

        fig, ax= plt.subplots(figsize=(8,8))
        plt.subplots_adjust(bottom=0.3)
        total = list(time_group_by_ph_and_col[ph].values())
        if 'NA' in time_group_by_ph_and_col[ph]:
            total[-1] = 0 

        tt = time_group_by_ph[ph]/len(tbl_group_by_ph[ph]['body_segment'].unique()) # timestamps are duplicated in the table for each of the body segments
        tt_string = f'{np.round(tt/(60*60), 0)}h {np.round(tt%(60*60)/60, 0)}m {np.round(tt%60, 0)}s'

        plt.title(f'{ph} - {tt_string}', fontsize=20)
        plt.gca().axis("equal")
        patches, texts = pie = plt.pie(total, startangle=5)
        labels = list(time_group_by_ph_and_col[ph].keys())
        labels_full = [f'{key:>8} - {np.round(value,2):>6}%' for key, value in time_group_by_ph_and_col[ph].items()]

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        arrowprops=dict(arrowstyle="-",connectionstyle="angle,angleA=0,angleB=90")
        kw = dict(xycoords='data',textcoords='data',arrowprops=arrowprops, 
                  bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(patches):
            ang = (p.theta2 - p.theta1)/2.+p.theta1
            y = np.sin(ang/180.*np.pi)
            x = 1.35*np.sign(np.cos(ang/180.*np.pi))
            if i == len(patches)-1 and 'NA' in time_group_by_ph_and_col[ph]:
                continue
            plt.gca().annotate(labels[i], xy=(0, 0), xytext=( x, y), **kw )

        plt.legend(pie[0],labels_full, loc="center", bbox_to_anchor=(1.5,0.5))
        plt.show()


def plot_raw_shimmer_data_for_symptom(symptom='tremor', area='RightUpperLimb', plot_first_x=5, df_all=None, df_all_subject_id=None):
    tbl = read_table(_PATHS.shimmer_task_tbl_path)
    sensor_list = ["back", "leftAnkle", "rightAnkle", "leftWrist", "rightWrist"]
    axis_list = ["X", "Y", "Z"]
    sub_tbl = tbl[np.logical_and(tbl['phenotype'] == symptom, tbl['body_segment'] == area)]

    for j, [index, row] in enumerate(sub_tbl.iterrows()):
        if j < plot_first_x:
            # print(dict(row))
            subject_id = row['subject_id'].split("_")[0]
            time_start = row['timestamp_start']
            time_end = row['timestamp_end']
            score = row['score']
            if df_all_subject_id != subject_id or df_all is None:
                df_all = get_labelled_raw_shimmer_data_for_patient(patient_id=subject_id, display_frames = False)
                df_all_subject_id = subject_id
            corr_raw_data = df_all[np.logical_and(df_all['timestamp'] >= time_start, df_all['timestamp'] < time_end)]
            # count = len(corr_raw_data)
            # print(f"Number of datapoints {symptom}-{area}-{score} - {count}")
            
            fig, ax = plt.subplots(1, len(sensor_list), figsize=(5*len(sensor_list), 5))
            for i, sensor in enumerate(sensor_list):
                for axis in axis_list:
                    sensor_axis = f"{sensor}_{axis}"
                    ax[i].plot(np.arange(len(corr_raw_data[sensor_axis]))*0.02, 
                               list(corr_raw_data[sensor_axis]))
                ax[i].set_title(f'{sensor}', fontsize=20)
            plt.suptitle(f'{symptom}-{area}-{score}', fontsize=22, y=1.05)
                
            # print(list(corr_raw_data[sensor_axis]))
    plt.show()

    return df_all, df_all_subject_id
