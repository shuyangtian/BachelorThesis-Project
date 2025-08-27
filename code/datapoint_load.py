import torch 
from attrdict import AttrDict
import torch 
import os,glob
import numpy as np


_LISTS = AttrDict()
_LISTS.checkpoint_fea_list = ['timestamp','back_X ','back_Y','back_Z','back_Magnitude','leftAnkle_Magnitude ',
                             'leftAnkle_X','leftAnkle_Y','leftAnkle_Z','rightAnkle_Magnitude','rightAnkle_X ',
                             'rightAnkle_Y','rightAnkle_Z','leftWrist_Magnitude','leftWrist_X','leftWrist_Y','leftWrist_Z',
                             'rightWrist_Magnitude','rightWrist_X','rightWrist_Y','rightWrist_Z ','task_code',
                             'tremor_RightUpperLimb','tremor_LeftUpperLimb','tremor_RightLowerLimb','tremor_LeftLowerLimb',
                                                  'dyskinesia_RightUpperLimb','dyskinesia_LeftUpperLimb','dyskinesia_RightLowerLimb','dyskinesia_LeftLowerLimb',
                             'bradykinesia_RightUpperLimb','bradykinesia_LeftUpperLimb','bradykinesia_RightLowerLimb','bradykinesia_LeftLowerLimb']


def print_fea():
    print('\ncheckpoint_fea list:')
    print(_LISTS.checkpoint_fea_list)

def get_all_chekpoints(checkpoint_fea, display_frames = False):
    
    dir =  '/home/stian/code/codetest/data/shimmer_data_windowsz-5_overlap-1'
    
    feature_data = []
    
    feature = checkpoint_fea
    
    print('feature:',feature)
    print('read: \n')
    
    for file in glob.glob(dir + '/*.torch'):
        print(file)
        
        checkpoint = torch.load(file)
        if feature not in checkpoint:
            print('the feature not exist')
            
        f_data = checkpoint[feature]
        feature_data.append(f_data)
        
    if len(feature_data) > 0:
        feature_data = np.array(feature_data)
        print(feature_data.shape)
        
    return feature_data

def get_all_chekpoints_reduce(checkpoint_fea,reduce):
    
    dir =  '/home/stian/code/codetest/data/shimmer_data_windowsz-5_overlap-1'
    
    feature_data = []
    
    feature = checkpoint_fea
    
    print('feature:',feature)
    print('read: \n')
    
    for file in glob.glob(dir + '/*.torch'):
        print(file)
        
        checkpoint = torch.load(file)
        if feature not in checkpoint:
            print('the feature not exist')
            
        f_data = checkpoint[feature]
        feature_data.append(f_data)
        
    if len(feature_data) > 0:
        feature_data = np.array(feature_data)
        feature_data = feature_data[:,::reduce]
        print(feature_data.shape)
        
    return feature_data


def acc_rms(x,y,z):
    return np.sqrt( ((x.astype(float))**2 / len(x) )+ ((y.astype(float))**2 /len(x))+ ((z.astype(float))**2 / len(x)))
