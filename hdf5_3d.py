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
        self.meshType
        if not os.path.isfile(filename):
            filename='%s %s' %(filename.split(".h5",1)[0],".H5")
            if not os.path.isfile(filename):
                print("%s file do not exists" % (filename))
    def loadDataStructure (self):
        file = h5py.File(filename, 'r')
        self.numTimeSteps=file[dataset_numTimeSteps][(0)]
        dataVolumes=file[dataset_Volumes]
        if dataVolumes.shape == 1
            self.meshType='structured'
            Volumes=np.array(dataVolumes[()])
        else 
            self.meshType='unstructured'
            Volumes=np.array(dataVolumes[()])
    

        
            
def calcoloMagnMedia(time,file,versoreu,versorev,versorew):
		data=np.array([])
		dataset_Magnet   = '/Emme%s/Val'%(time)
		dataset_Hext   = '/Hext%s/Val'%(time)
		#print(dataset_Magnet)
		datasetM = file[dataset_Magnet]
		#print(datasetM.shape, isinstance(datasetM,h5py.Dataset))
		#magnetizzazione  = np.matrix(datasetM[0:103,:])
		magnetizzazione  = np.matrix(datasetM[()])
	
		#print(np.shape(magnetizzazione))
		proiezu=np.dot(magnetizzazione,versoreu)
		proiezv=np.dot(magnetizzazione,versorev)
		proiezw=np.dot(magnetizzazione,versorew)
		#print(proiezw,i, "\n")
		datasetH = file[dataset_Hext]
		#print(datasetH.shape, isinstance(datasetH,h5py.Dataset))
		#Hext= datasetH[0:103,0]
		Hext= datasetH[(0)]
		Hext=np.dot(np.dot(Hext,versoreu),np.reshape((1,0,0),(1,3)))+np.dot(np.dot(Hext,versorev),np.reshape((0,1,0),(1,3)))+np.dot(np.dot(Hext,versorew),np.reshape((0,0,1),(1,3)))
		np.savetxt("uffa",proiezu)
		#print(Hext)
		Volumes=np.ones(proiezu.shape[0])*(6.5e-9*6.5e-9*7.e-9)
		mediau=np.average(proiezu,axis=0,weights=Volumes)
		mediav=np.average(proiezv,axis=0,weights=Volumes)
		mediaw=np.average(proiezw,axis=0,weights=Volumes)
		data=np.append(data,[Hext[0],mediau,Hext[1],mediav,Hext[2],mediaw])
    return data


if  __name__ == '__main__':
    mainDir = "C:\\Users\\r.ferrero\\Desktop\\fast"
    filename= "dot_280_s28_hy.h5"
    outputfile=filename.split(".", 1)[0]+".dat"
    outputfile=outputfile.split("_", 1)[0]+"_Hyst_"+outputfile.split("_", 1)[1]
    print(outputfile)
    hdf5_file_name = os.path.join(mainDir, filename)

    

    event_number   = 5
    
    versoreu=np.array([[0.86602],[0],[0.50001]])
    versorev=np.array([[0],[1],[0]])
    versorew=np.array([[-0.50001],[0],[0.86602]])
    versoreT=np.reshape(versore,(1,3))
    file    = h5py.File(hdf5_file_name, 'r')   # 'r' means that hdf5 file is open in read-only mode
    file.visit()
    datasetTime=file[dataset_numTimeSteps]
    #datasetVol=file[dataset_Volumes]
    numTimeSteps= datasetTime[(0)]
    print(numTimeSteps)
    mediau= np.array([])
    mediav= np.array([])
    mediaw= np.array([])
    Hexternal=np.array([])
    outputdata=np.array([])
    Volumes=np.array(datasetVol[()])
    for i in range(1,numTimeSteps[0]):

        outputdata=np.append(outputdata,calcoloMagnMedia(int(i),file,versoreu,versorev,versorew))
        
    print(np.shape(outputdata) , "np.shape outputdata")
    outputdata=np.reshape(outputdata,(-1,6))
    np.savetxt(outputfile, outputdata, fmt='%26.18e')

    file.close()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    lb = "u"
    ax.plot(outputdata[:,0], outputdata[:,1],label=lb)
    lb = "v"
    ax.plot(outputdata[:,2], outputdata[:,3],label=lb)
    lb = "w"
    ax.plot(outputdata[:,4], outputdata[:,5],label=lb)
    ax.legend(numpoints=1)
    ax.grid(True)
    #plt.plot(Hexternal, mediau)
    plt.show()
    #




