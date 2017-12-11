import glob, os, sys
import numpy as np
import scipy.integrate as integrate
import scipy.ndimage
import matplotlib.pylab as plt
from scipy.interpolate import griddata

def integra(x,y,method='simps'):
        fullHyst = x[-1] == x[0]
        if fullHyst:
           middle=int(np.round(x.size/4))
           top=int(np.round(x.size/2))
           if method=='simps':
               branchup=integrate.simps(y[0:middle],x[0:middle])
               branchdown=integrate.simps(y[middle:top],x[middle:top])
           else:
               branchup=integrate.trapz(y[0:middle],x[0:middle])
               branchdown=integrate.trapz(y[middle:top],x[middle:top])   
           result=-branchdown-branchup
        else:
            if method=='simps':
                branchdown=integrate.simps(y,x)
                branchup=integrate.simps(-np.flipud(y),-np.flipud(x))
            else:
                branchdown=integrate.trapz(y,x)
                branchup=integrate.trapz(-np.flipud(y),-np.flipud(x))
            result=(-branchdown+branchup)/2
        return result



class Integral:
    """
    Standalone version of integrate class
    This class load the data given a filename and integrates the curve
    """
    def __init__(self, filename, mainDir, is_avoid_zeros=True):
        # It is better to make general x,y arrays
        self._mainDir = mainDir
        fname = os.path.join(self._mainDir, filename)
        self.x, self.y = np.loadtxt(fname , comments="#", unpack=True)
        if is_avoid_zeros:
            s_len = len(self.x)
            self.x, self.y = self.avoid_zeros()
            print("%i lines deleted" % (s_len - len(self.x)))
        
        self.value=integra(self.x, self.y)
        self.energy=2*4*np.pi*1.e-7* self.value

    def avoid_zeros(self):
        is_not_zero = self.y != 0
        x = self.x[is_not_zero]
        y = self.y[is_not_zero]
        return x, y

if __name__ == "__main__":
    mainDir = "W:\\Micro\\Riccardo\\Dot\\Single\\Results\\Hyst_new\\Bis"
    filename="dot_Hy_650_t25_bis.dat"
    integ=Integral(filename,mainDir)
    #energy=2*4*np.pi*1.e-7*integ.value
    dati=np.array([])
    dati=np.append(dati,(int(150),int(50),float(2),integ.energy))
    dati=np.reshape(dati,(-1,4))
    print(dati)
    outputfile=filename.split(".", 1)[0]+".dat"
    outputfile="Energy_"+outputfile
    np.savetxt(outputfile,dati,fmt='%4d %4d %4.2f %12.8e',header='diametro numero concentrazione energia')
    print(integ.energy)
