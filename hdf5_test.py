import glob, os, sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

"""
Basic script Open a HDF5 file of my simulation and compute the Hysteresis loop, saves data in an opportune file with specific naming pattern
at the end plots the calculated loop.
"""
def calcoloMagnMedia(time,file,Volumes,versoreu,versorev,versorew):
    data=np.array([])
    dataset_Magnet   = '/Magnetizzazione%s/Val'%(time)
    dataset_Hext   = '/Hext%s/Val'%(time)
    #print(dataset_Magnet)
    datasetM = file[dataset_Magnet]
    #print(datasetM.shape, isinstance(datasetM,h5py.Dataset))
    #magnetizzazione  = np.matrix(datasetM[0:103,:])
    magnetizzazione  = np.matrix(datasetM[()])

    #print(np.shape(magnetizzazione))
    #proiez=np.dot(np.dot(magnetizzazione,versore),versoreT)

    proiezu = np.dot(magnetizzazione, versoreu)
    proiezv = np.dot(magnetizzazione, versorev)
    proiezw = np.dot(magnetizzazione, versorew)

    #print(proiez,i, "\n")
    datasetH = file[dataset_Hext]
    #print(datasetH.shape, isinstance(datasetH,h5py.Dataset))
    #Hext= datasetH[0:103,0]
    Hext= datasetH[(0)]
    Hext = np.dot(np.dot(Hext, versoreu), np.reshape((1, 0, 0), (1, 3))) + np.dot(np.dot(Hext, versorev),
                                                                                  np.reshape((0, 1, 0),
                                                                                             (1, 3))) + np.dot(
        np.dot(Hext, versorew), np.reshape((0, 0, 1), (1, 3)))
    #np.savetxt("uffa",proiezu)
    mediau=np.average(proiezu,weights=Volumes)
    mediav=np.average(proiezv,weights=Volumes)
    mediaw=np.average(proiezw,weights=Volumes)

    data=np.append(data, [Hext[0], mediau, Hext[1], mediav, Hext[2], mediaw])
    return data

def calcoloMagnMediaDisks(time,file,Volumes,numObj,versoreu,versorev,versorew):
    data=np.array([])
    dataset_Magnet   = '/Magnetizzazione%s/Val'%(time)
    dataset_Hext   = '/Hext%s/Val'%(time)
    #print(dataset_Magnet)
    datasetM = file[dataset_Magnet]
    #print(datasetM.shape, isinstance(datasetM,h5py.Dataset))
    #magnetizzazione  = np.matrix(datasetM[0:103,:])
    magnetizzazione  = np.matrix(datasetM[()])

    #print(np.shape(magnetizzazione))
    #proiez=np.dot(np.dot(magnetizzazione,versore),versoreT)

    proiezu = np.dot(magnetizzazione, versoreu)
    proiezv = np.dot(magnetizzazione, versorev)
    proiezw = np.dot(magnetizzazione, versorew)

    #print(Volumes[9:12], "\n")
    datasetH = file[dataset_Hext]
    #print(datasetH.shape, isinstance(datasetH,h5py.Dataset))
    #Hext= datasetH[0:103,0]
    Hext= datasetH[(0)]
    Hext = np.dot(np.dot(Hext, versoreu), np.reshape((1, 0, 0), (1, 3))) + np.dot(np.dot(Hext, versorev),
                                                                                  np.reshape((0, 1, 0),
                                                                                             (1, 3))) + np.dot(
        np.dot(Hext, versorew), np.reshape((0, 0, 1), (1, 3)))
    #np.savetxt("uffa",proiezu)
    numElem=int(np.size(magnetizzazione,0)/numObj)
    for i in range(1, numObj+1):
        mediau=np.average(proiezu[(i-1)*numElem : i*numElem-1],weights=Volumes[(i-1)*numElem:i*numElem-1])
        mediav=np.average(proiezv[(i-1)*numElem : i*numElem-1],weights=Volumes[(i-1)*numElem:i*numElem-1])
        mediaw=np.average(proiezw[(i-1)*numElem : i*numElem-1],weights=Volumes[(i-1)*numElem:i*numElem-1])
        data=np.append(data, [Hext[0], mediau, Hext[1], mediav, Hext[2], mediaw])
    return data

def calcoloEnergia(time,file,Volumes):
    data=np.array([])
    dataset_Magnet   = '/Magnetizzazione%s/Val'%(time)
    dataset_Hext   = '/Hext%s/Val'%(time)
    dataset_Hms = '/Hms%s/Val'% (time)


    #print(dataset_Magnet)
    datasetM = file[dataset_Magnet]
    data_hms= file[dataset_Hms]
    hms=np.matrix(data_hms[()])
    data_Hext = file[dataset_Hms]
    hext = np.matrix(data_Hext[()])

 #   magnetizzazione  = np.matrix(datasetM[0:103,:])
    magnetizzazione  = np.matrix(datasetM[()])

    enHms=-2*np.pi*1.e-7*np.einsum('ij, ij->i', hms, magnetizzazione)
    enHms =np.reshape(enHms, (-1, 1))
    enHms= np.average(enHms,weights=Volumes)
    enZee=-4*np.pi*1.e-7*np.einsum('ij, ij->i',magnetizzazione, hext)
    enZee =np.reshape(enZee, (-1, 1))
    enZee= np.average(enZee,weights=Volumes)

    #print(proiez,i, "\n")
    datasetH = file[dataset_Hext]

    data=np.append(data,[time, enHms,enZee])
    return data

class hdf5_test:
    def __init__(self,mainDir,filename,numObj=1,versoreu = np.array([[1],[0],[0]]),versorev = np.array([[0],[1],[0]]),versorew = np.array([[0],[0],[1]])):
        self.mainDir=mainDir
        outputfile=filename.split(".", 1)[0]+".dat"
        self.outputHystfile=f'{outputfile.split("_", 1)[0]}_Hyst_{outputfile.split("_", 1)[1]}'
        self.outputEnergyfile=f'{outputfile.split("_", 1)[0]}_Energy_{outputfile.split("_", 1)[1]}'
        print(outputfile)
        hdf5_file_name = os.path.join(mainDir, filename)


        dataset_numTimeSteps ='/Timesteps/TimeSteps#'
        dataset_Volumes ='/Volumes'
        #event_number   = 5


        self.file    = h5py.File(hdf5_file_name, 'r')   # 'r' means that hdf5 file is open in read-only mode

        datasetTime=self.file[dataset_numTimeSteps]
        datasetVol=self.file[dataset_Volumes]
        self.numTimeSteps= datasetTime[(0)]
        print(self.numTimeSteps)
        self.mediau= np.array([])
        self.mediav= np.array([])
        self.mediaw= np.array([])
        self.Hexternal=np.array([])
        self.outputdata=np.array([])
        self.outputdata2 = np.array([])
        self.outputEner=np.array([])
        self.Volumes=np.array(datasetVol[()])
        self.u=versoreu
        self.v=versorev
        self.w=versorew
    # for i in range(1,numTimeSteps):
    #          #outputdata=np.append(outputdata,calcoloMagnMedia(int(i),file,Volumes))
    #          #outputEner = np.append(outputEner, calcoloEnergia(int(i), file, Volumes))
    #          outputdata = np.append(outputdata, calcoloMagnMediaDisks(int(i), file, Volumes,numObj))
    # print(np.shape(outputdata) , "np.shape outputdata")
    #
    # outputdata = np.reshape(outputdata, (-1, 6*(numObj)))
    # #outputEner = np.reshape(outputEner, (-1, 3))
    # #np.savetxt(os.path.join(mainDir, outputHystfile), outputdata, fmt='%26.18e')
    # #np.savetxt(os.path.join(mainDir, outputEnergyfile), outputEner, fmt='%26.18e')
    # for i in range(1, numObj+1):
    #     outputHystfile = outputfile.split("_", 1)[0] + "_Hyst_" + str(i) +"_"+ outputfile.split("_", 1)[1]
    #     np.savetxt(os.path.join(mainDir, outputHystfile), outputdata[:, (i-1)*6:i*6], fmt='%26.18e')


    def compute(self):
        for i in range(0,self.numTimeSteps):
                 self.outputdata2=np.append(self.outputdata2,calcoloMagnMedia(int(i),self.file,self.Volumes,self.u,self.v,self.w))
                 #outputEner = np.append(outputEner, calcoloEnergia(int(i), file, Volumes))
                 #outputdata = np.append(outputdata, calcoloMagnMediaDisks(int(i), file, Volumes,numObj))
        print(np.shape(self.outputdata2) , "np.shape outputdata")

        self.outputdata2 = np.reshape(self.outputdata2, (-1, 6))
        #outputEner = np.reshape(outputEner, (-1, 3))
        #np.savetxt(os.path.join(mainDir, outputHystfile), outputdata, fmt='%26.18e')
        #np.savetxt(os.path.join(mainDir, outputEnergyfile), outputEner, fmt='%26.18e')

        np.savetxt(os.path.join(self.mainDir, self.outputHystfile), self.outputdata2, fmt='%26.18e')

        self.file.close()

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        lb = "u"
        ax.plot(self.outputdata2[1:-1, 0]/1000, self.outputdata2[1:-1, 1]/1000, label=lb)
        lb = "v"
        ax.plot(self.outputdata2[1:-1, 2]/1000, self.outputdata2[1:-1, 3]/1000, label=lb)
        lb = "w"
        ax.plot(self.outputdata2[1:-1, 4]/1000, self.outputdata2[1:-1, 5]/1000, label=lb)
        ax.legend(numpoints=1)
        ax.grid(True)
        #plt.plot(Hexternal, mediau)
        plt.show()

def main():
    #mainDir = "W:\\Micro\\Riccardo\\cfr2d3d_3d_random\\2d3d"
    mainDir = "S:\\Alessandra\\2d3d\\Thermal"
    #mainDir= "W:\\Micro\\2d3d\\SquarePerCfr3D"
    #mainDir = "W:\\Micro\\Riccardo\\cfr2d3d_3d_random\\approx_noapprox"
    #mainDir = "W:\\Micro\\2d3d\\dot150\\n54"
    #mainDir = "W:\\Micro\\FePd\\d250"
    mainDir= "W:\\Micro\\magnetite\\disks"
    filename= "d150t30n50c21_1.h5"
    hystcalc=hdf5_test(mainDir,filename,numObj=50)
    hystcalc.compute()
    hystcalc.plot()

if  __name__ == '__main__':
    main()


