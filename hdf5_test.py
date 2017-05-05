import glob, os, sys
import h5py
import numpy as np

mainDir = "C:\\Projects\\Git\\Python-In-The-Lab_Project\\Hyst"
filename= "dot_200_00_s30.h5"
hdf5_file_name = os.path.join(mainDir, filename)
#hdf5_file_name = '/reg/d/psdm/XPP/xppcom10/hdf5/xppcom10-r0546.h5'
dataset_name   = '/Magnetizzazione100/Val'
event_number   = 5

file    = h5py.File(hdf5_file_name, 'r')   # 'r' means that hdf5 file is open in read-only mode




dataset = file[dataset_name]
print(dataset.shape, isinstance(dataset,h5py.Dataset))
arr1ev  = dataset[()]
file.close()

#print ('arr1ev.shape =', arr1ev.shape)
print ('arr1ev =\n',     arr1ev)