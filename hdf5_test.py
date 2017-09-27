import glob, os, sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

"""
Basic script Open a HDF5 file of my simulation and compute the Hysteresis loop, saves data in an opportune file with specific naming pattern
at the end plots the calculated loop.
"""

mainDir = "C:\\Projects\\Git\\Python-In-The-Lab_Project\\Hyst"
filename= "dot_200_00_s30.h5"
outputfile=filename.split(".", 1)[0]+".dat"
outputfile=outputfile.split("_", 1)[0]+"_Hyst_"+outputfile.split("_", 1)[1]
print(outputfile)
hdf5_file_name = os.path.join(mainDir, filename)
#hdf5_file_name = '/reg/d/psdm/XPP/xppcom10/hdf5/xppcom10-r0546.h5'

dataset_numTimeSteps ='/Timesteps/TimeSteps#'
dataset_Volumes ='/Volumes'
event_number   = 5

versore=np.array([[1],[0],[0]])
versoreT=np.reshape(versore,(1,3))
file    = h5py.File(hdf5_file_name, 'r')   # 'r' means that hdf5 file is open in read-only mode

datasetTime=file[dataset_numTimeSteps]
datasetVol=file[dataset_Volumes]
numTimeSteps= datasetTime[(0)]
print(numTimeSteps)
mediau= np.array([])
mediav= np.array([])
mediaw= np.array([])
Hexternal=np.array([])
outputdata=np.array([])
Volumes=np.array(datasetVol[()])
for i in range(1,numTimeSteps):
    dataset_Magnet   = '/Magnetizzazione%s/Val'%(i)
    dataset_Hext   = '/Hext%s/Val'%(i)
    #print(dataset_Magnet)
    datasetM = file[dataset_Magnet]
    #print(datasetM.shape, isinstance(datasetM,h5py.Dataset))
    #magnetizzazione  = np.matrix(datasetM[0:103,:])
    magnetizzazione  = np.matrix(datasetM[()])

    #print(np.shape(magnetizzazione))
    proiez=np.dot(np.dot(magnetizzazione,versore),versoreT)
    #print(proiez,i, "\n")
    datasetH = file[dataset_Hext]
    #print(datasetH.shape, isinstance(datasetH,h5py.Dataset))
    #Hext= datasetH[0:103,0]
    Hext= datasetH[(0)]
    np.savetxt("uffa",proiez)
    mediau=np.append(mediau,np.average(proiez[:,0],weights=Volumes))
    mediav=np.append(mediav,np.average(proiez[:,1],weights=Volumes))
    mediaw=np.append(mediaw,np.average(proiez[:,2],weights=Volumes))
    Hexternal=np.append(Hexternal,Hext[0])
    outputdata=np.append(outputdata,(Hexternal[i-1],mediau[i-1],mediav[i-1],mediaw[i-1]))
    
    #endforloop
print(np.shape(outputdata) , "np.shape outputdata")
outputdata=np.reshape(outputdata,(-1,4))
np.savetxt(outputfile, outputdata,, fmt='%26.18e')

file.close()
#print(Hexternal)
fig = plt.figure()
ax = fig.add_subplot(111)
lb = "u"
ax.plot(Hexternal, mediau,label=lb)
lb = "v"
ax.plot(Hexternal, mediav,label=lb)
lb = "w"
ax.plot(Hexternal, mediaw,label=lb)
ax.legend(numpoints=1)
ax.grid(True)
#plt.plot(Hexternal, mediau)
plt.show()
#
# print ('arr1ev.shape =', arr1ev.shape)
#print ('\n media =', media,'\n versore =', versore)



