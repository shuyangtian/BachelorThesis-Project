import numpy as np
import pandas
import os, sys
import torch
import matplotlib.pyplot as plt
from attrdict import AttrDict

from global_constants import _PATHS, _LISTS, _CONSTS
from data_loading import *
from data_visualization import *

def create_shimmer_data_dict(pat_ids=None, window_sec=5, overlap_sec=1):
    """ Y = shimmer labels (tbl_task_sc_2.csv)
    """

    window_step_sec = window_sec - overlap_sec

    shimmer_tbl = read_table(table_file_path=_PATHS.shimmer_task_tbl_path)
  


    counts = []
    file_size = 0

    action_tbl = read_table(table_file_path=_PATHS.action_dict_path)
    action_dict = {code: row_id for [code, row_id] in zip(action_tbl["task_code"].to_numpy(), action_tbl["ROW_ID"].to_numpy())}

    data_dir = os.path.join('data', f"shimmer_data_windowsz-{window_sec}_overlap-{overlap_sec}")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if pat_ids is None:
        pat_ids = np.unique(shimmer_tbl['subject_id'].to_numpy())
        for i, pat_id in enumerate(pat_ids):
            pat_ids[i] = pat_id.split('_')[0]

    for pat_id in pat_ids:

        print(f"Patient ID: {pat_id}")

        raw_data = get_raw_shimmer_data_for_patient(patient_id=pat_id)
        tbl_sub_pat = shimmer_tbl[shimmer_tbl['subject_id']==f'{pat_id}_BOS']

        all_times = np.stack([tbl_sub_pat['timestamp_start'], tbl_sub_pat['timestamp_end']], axis=-1)
        times, cnts = np.unique(all_times, return_counts=True, axis=0)
        print('No. of unique timestamp pairs * No. of body parts = ', len(times), '* 12 = ', len(times)*12)

        count = 0
        for j, [time_start, time_end] in enumerate(times):

            if time_end - time_start < window_sec:
                continue
            # print(dict(row))

            tbl_sub_pat_sub_time = tbl_sub_pat[np.logical_and(tbl_sub_pat['timestamp_start'] == time_start, tbl_sub_pat['timestamp_end'] == time_end)]
            Y_dict = AttrDict()

            Y = AttrDict()
            if "task_code" not in Y:
                val = tbl_sub_pat_sub_time["task_code"].to_numpy()[0]
                Y["task_code"] = np.array(val)
                    
            for _, [_, row] in enumerate(tbl_sub_pat_sub_time.iterrows()):
                # print(row)
                score = row["score"]
                Y[f'{row["phenotype"]}_{row["body_segment"]}'] = np.array(score)

            for time_start_sub in np.arange(time_start, time_end-window_sec, window_step_sec):

                corr_raw_data = raw_data[np.logical_and(raw_data['timestamp'] >= time_start_sub, raw_data['timestamp'] < time_start_sub + window_sec)]
                data_dict = AttrDict()
                for key in corr_raw_data.keys():
                    data_dict[key] = corr_raw_data[key].to_numpy()
                data_dict.update(Y)

                count += 1

                file_name = f'{pat_id}_BOS-shimmer-{count}.torch'
                torch.save(data_dict, os.path.join(data_dir, file_name))

                counts.append(count)

                if count == 1:
                    path = "example.torch"
                    torch.save(data_dict, path)
                    file_size = os.path.getsize(path)

    counts = np.stack(counts)            
    return counts, file_size

def create_smartdevice_dataset():
    """ Y = smartdevice labels (tbl_task_sc_1.csv)
    """
    return


if __name__ == '__main__':

    counts, file_size = create_shimmer_data_dict()
    print("No. of datapoints: ", counts.sum(), " File size of each datapoint: ", file_size, " Total file size: ", counts.sum()*file_size)
