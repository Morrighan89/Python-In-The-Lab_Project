import glob, os, sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

"""
Basic script Open a HDF5 file of my simulation and compute the Hysteresis loop, saves data in an opportune file with specific naming pattern
at the end plots the calculated loop.
"""
def calcoloMagnMedia(time,file,Volumes):
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

def calcoloMagnMediaDisks(time,file,Volumes,numDisks):
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
    numElem=int(np.size(magnetizzazione,0)/numDisks)
    for i in range(1, numDisks+1):
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
if  __name__ == '__main__':
    #mainDir = "W:\\Micro\\Riccardo\\cfr2d3d_3d_random\\2d3d"
    mainDir = "S:\\Alessandra\\2d3d\\Thermal"
    #mainDir= "W:\\Micro\\2d3d\\SquarePerCfr3D"
    #mainDir = "W:\\Micro\\Riccardo\\cfr2d3d_3d_random\\approx_noapprox"
    #mainDir = "W:\\Micro\\2d3d\\dot150\\n54"
    #mainDir = "W:\\Micro\\FePd\\d250"
    filename= "temp150n30c27d3cont_1.h5"
    outputfile=filename.split(".", 1)[0]+".dat"
    outputHystfile=outputfile.split("_", 1)[0]+"_Hyst_"+outputfile.split("_", 1)[1]
    outputEnergyfile=outputfile.split("_", 1)[0]+"_Energy_"+outputfile.split("_", 1)[1]
    print(outputfile)
    hdf5_file_name = os.path.join(mainDir, filename)

    
    dataset_numTimeSteps ='/Timesteps/TimeSteps#'
    dataset_Volumes ='/Volumes'
    event_number   = 5

    versoreu = np.array([[1],[0],[0]])
    versorev = np.array([[0], [1], [0]])
    versorew = np.array([[0],[0],[1]])


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
    outputdata2 = np.array([])
    outputEner=np.array([])
    Volumes=np.array(datasetVol[()])
    numDisks=30
    # for i in range(1,numTimeSteps):
    #          #outputdata=np.append(outputdata,calcoloMagnMedia(int(i),file,Volumes))
    #          #outputEner = np.append(outputEner, calcoloEnergia(int(i), file, Volumes))
    #          outputdata = np.append(outputdata, calcoloMagnMediaDisks(int(i), file, Volumes,numDisks))
    # print(np.shape(outputdata) , "np.shape outputdata")
    #
    # outputdata = np.reshape(outputdata, (-1, 6*(numDisks)))
    # #outputEner = np.reshape(outputEner, (-1, 3))
    # #np.savetxt(os.path.join(mainDir, outputHystfile), outputdata, fmt='%26.18e')
    # #np.savetxt(os.path.join(mainDir, outputEnergyfile), outputEner, fmt='%26.18e')
    # for i in range(1, numDisks+1):
    #     outputHystfile = outputfile.split("_", 1)[0] + "_Hyst_" + str(i) +"_"+ outputfile.split("_", 1)[1]
    #     np.savetxt(os.path.join(mainDir, outputHystfile), outputdata[:, (i-1)*6:i*6], fmt='%26.18e')



    for i in range(1,numTimeSteps):
             outputdata2=np.append(outputdata2,calcoloMagnMedia(int(i),file,Volumes))
             #outputEner = np.append(outputEner, calcoloEnergia(int(i), file, Volumes))
             #outputdata = np.append(outputdata, calcoloMagnMediaDisks(int(i), file, Volumes,numDisks))
    print(np.shape(outputdata2) , "np.shape outputdata")

    outputdata2 = np.reshape(outputdata2, (-1, 6))
    #outputEner = np.reshape(outputEner, (-1, 3))
    #np.savetxt(os.path.join(mainDir, outputHystfile), outputdata, fmt='%26.18e')
    #np.savetxt(os.path.join(mainDir, outputEnergyfile), outputEner, fmt='%26.18e')
    outputHystfile = outputfile.split("_", 1)[0] + "_Hyst_" + outputfile.split("_", 1)[1]
    np.savetxt(os.path.join(mainDir, outputHystfile), outputdata2, fmt='%26.18e')

    file.close()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    lb = "u"
    ax.plot(outputdata2[1:-1, 0]/1000, outputdata2[1:-1, 1]/1000, label=lb)
    lb = "v"
    ax.plot(outputdata2[1:-1, 2]/1000, outputdata2[1:-1, 3]/1000, label=lb)
    lb = "w"
    ax.plot(outputdata2[1:-1, 4]/1000, outputdata2[1:-1, 5]/1000, label=lb)
    ax.legend(numpoints=1)
    ax.grid(True)
    #plt.plot(Hexternal, mediau)
    plt.show()





