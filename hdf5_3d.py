import glob, os, sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import mysettings

"""
Basic script Open a HDF5 file of my simulation and compute the Hysteresis loop, saves data in an opportune file with specific naming pattern
at the end plots the calculated loop.
"""

class Soluzione:
    """
    This class load the data given a filename
    and gives the possibility to generate a plot with the uploaded data
    """
    def __init__(self, filename):
        # It is better to make general x,y arrays
        
        if not os.path.isfile(filename):
            filename='%s %s' %(filename.split(".h5",1)[0],".H5")
            if not os.path.isfile(filename):
                print("%s file do not exists" % (filename))
    def loadDataStructure (self):
        file = h5py.File(filename, 'r')

        
            
def calcoloMagnMedia(time,file,Volumes):
    data=np.array([])
    dataset_Magnet   = '/Emme%s/Val'%(time)
    dataset_Hext   = '/Hext%s/Val'%(time)
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
    mediau=np.average(proiez[:,0])
    mediav=np.average(proiez[:,1])
    mediaw=np.average(proiez[:,2])
    data=np.append(data,[Hext[0],mediau,mediav,mediaw])
    return data

if  __name__ == '__main__':
    mainDir = "C:\\Users\\r.ferrero\\Desktop\\fast"
    filename= "dot_280_s28_hy.h5"
    outputfile=filename.split(".", 1)[0]+".dat"
    outputfile=outputfile.split("_", 1)[0]+"_Hyst_"+outputfile.split("_", 1)[1]
    print(outputfile)
    hdf5_file_name = os.path.join(mainDir, filename)

    

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

        outputdata=np.append(outputdata,calcoloMagnMedia(int(i),file,Volumes))
        
    print(np.shape(outputdata) , "np.shape outputdata")
    outputdata=np.reshape(outputdata,(-1,4))
    np.savetxt(outputfile, outputdata, fmt='%26.18e')

    file.close()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    lb = "u"
    ax.plot(outputdata[:,0], outputdata[:,1],label=lb)
    lb = "v"
    ax.plot(outputdata[:,0], outputdata[:,2],label=lb)
    lb = "w"
    ax.plot(outputdata[:,0], outputdata[:,3],label=lb)
    ax.legend(numpoints=1)
    ax.grid(True)
    #plt.plot(Hexternal, mediau)
    plt.show()
    #




