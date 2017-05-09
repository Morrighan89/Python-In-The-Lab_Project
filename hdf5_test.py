import glob, os, sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

mainDir = "C:\\Projects\\Git\\Python-In-The-Lab_Project\\Hyst"
filename= "dot_200_00_s30.h5"
outputfile=filename.split(".", 1)[0]+".dat"
outputfile=outputfile.split("_", 1)[0]+"_Hyst_"+outputfile.split("_", 1)[1]
print(outputfile)
hdf5_file_name = os.path.join(mainDir, filename)
#hdf5_file_name = '/reg/d/psdm/XPP/xppcom10/hdf5/xppcom10-r0546.h5'
dataset_Magnet   = '/Magnetizzazione100/Val'
dataset_Hext   = '/Hext0/Val'
dataset_numTimeSteps ='/Timesteps/TimeSteps#'
event_number   = 5

versore=np.array([[1],[0],[0]])
versoreT=np.reshape(versore,(1,3))
file    = h5py.File(hdf5_file_name, 'r')   # 'r' means that hdf5 file is open in read-only mode

datasetTime=file[dataset_numTimeSteps]
numTimeSteps= datasetTime[(0)]
print(numTimeSteps)
media= np.array([])
Hexternal=np.array([])
outputdata=np.array([])
for i in range(1,numTimeSteps):
    dataset_Magnet   = '/Magnetizzazione%s/Val'%(i)
    dataset_Hext   = '/Hext%s/Val'%(i)
    #print(dataset_Magnet)
    datasetM = file[dataset_Magnet]
    #print(datasetM.shape, isinstance(datasetM,h5py.Dataset))
    magnetizzazione  = np.matrix(datasetM[()])
    #print(np.shape(magnetizzazione))
    proiez=np.dot(np.dot(magnetizzazione,versore),versoreT)
    #print(proiez,i, "\n")
    datasetH = file[dataset_Hext]
    #print(datasetH.shape, isinstance(datasetH,h5py.Dataset))
    Hext= datasetH[(0)]
    
    np.savetxt("uffa",proiez)
    media=np.append(media,np.average(proiez[:,0]))
    Hexternal=np.append(Hexternal,Hext[0])
    outputdata=np.append(outputdata,(Hexternal[i-1],media[i-1]))
    
    #endforloop
print(np.shape(outputdata))
outputdata=np.reshape(outputdata,(-1,2))
np.savetxt(outputfile, outputdata)
#print("\n", media, "media shape \n")
file.close()
#print(Hexternal)
plt.plot(Hexternal, media)
plt.show()
#
# print ('arr1ev.shape =', arr1ev.shape)
#print ('\n media =', media,'\n versore =', versore)



