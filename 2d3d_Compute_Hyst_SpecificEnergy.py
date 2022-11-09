import glob, os, sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import hdf5_test
import Integration_Class

def main():
    mainDir= "W:\\Micro\\magnetite\\disks"
    filename= "d150t30n50c21_1.h5"
    u=np.array([[1],[0],[0]])
    v=np.array([[0],[1],[0]])
    w=np.array([[0],[0],[1]])
    hystcalc=hdf5_test.hdf5_test(mainDir,filename,numObj=50)
    hystcalc.compute()
    dati=[]
    integ=Integration_Class.Integral(hystcalc.outputHystfile,mainDir)
        #dati=np.array([])
    dati=np.append(dati,(int(150),int(30),integ.energy))
    dati=np.reshape(dati,(-1,3))
    print(dati)
    outputfile=f'SpecEnergy_{filename.split(".", 1)[0]}.dat'
    np.savetxt(os.path.join(mainDir, outputfile),dati,fmt='%4d %4d  %12.8e',header='diametro spessore energia')

if  __name__ == '__main__':
    main()