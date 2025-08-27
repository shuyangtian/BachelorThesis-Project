from attrdict import AttrDict

_PATHS = AttrDict()

_PATHS.root = "/mnt/cephfs/common/neha/MJFF_Levadopa"

_PATHS.shimmer_back_folder_name = "Shimmer_Back"
_PATHS.shimmer_leftankle_folder_name = "Shimmer_LeftAnkle"
_PATHS.shimmer_rightankle_folder_name = "Shimmer_RightAnkle"
_PATHS.shimmer_leftwrist_folder_name = "Shimmer_LeftWrist"
_PATHS.shimmer_rightwrist_folder_name = "Shimmer_RightWrist"

_PATHS.geneactiv_folder_name = "GENEActiv"
_PATHS.pebble_folder_name = "Pebble"
_PATHS.phone_folder_name = "Phone"

_PATHS.smartdevice_task_tbl_path = "tbl_task_sc_1.csv"
_PATHS.shimmer_task_tbl_path = "tbl_task_sc_2.csv"

_PATHS.action_dict_path = "tbl_task_sc_dict.csv"

_PATHS.med_path = "tbl_medication_diary.csv"
_PATHS.home_tasks_path = "tbl_home_tasks.csv"
_PATHS.metadata_lab_visits_path = "tbl_metadata_lab_visits.csv"
_PATHS.metadata_lab_visits_dict_path = "tbl_metadata_lab_visits_dict.csv"
_PATHS.sensor_grp_1_details_path = "tbl_sensor_1.csv"
_PATHS.sensor_grp_2_details_path = "tbl_sensor_2.csv"
_PATHS.slp_diary_path = "tbl_slp_diary.csv"
_PATHS.sub_diary_path = "tbl_sub_diary.csv"
_PATHS.sub_diary_dict_path = "tbl_sub_diary_dict.csv"
_PATHS.updrs_path = "tbl_updrs.csv"

_LISTS = AttrDict()

_LISTS.shimmer_locations = [
    _PATHS.shimmer_back_folder_name, 
    _PATHS.shimmer_leftankle_folder_name, 
    _PATHS.shimmer_rightankle_folder_name, 
    _PATHS.shimmer_leftwrist_folder_name, 
    _PATHS.shimmer_rightwrist_folder_name
    ]

_LISTS.shimmer_patient_list = ["3", "4", "5", "6", "7", "8", "9", "10",
                       "11", "12", "13", "14", "15", "16", "17",
                       "18", "19"]
_LISTS.day_list = ["1", "2", "3", "4"]

_CONSTS = AttrDict()

_CONSTS.data_sampling_rate = 50
