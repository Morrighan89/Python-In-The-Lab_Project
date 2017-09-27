import glob, os, sys
import numpy as np
import scipy.integrate as integrate
import scipy.ndimage
import matplotlib.pylab as plt
from scipy.interpolate import griddata


class integral:
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
        self.fullHyst=self.x[-1]-self.x[0]
        value=self.integra()
        self.energy=2*4*np.pi*1.e-7*value

    def avoid_zeros(self):
        is_not_zero = self.y != 0
        x = self.x[is_not_zero]
        y = self.y[is_not_zero]
        return x, y

    def integra(self):
        
        if self.fullHyst==0:
           middle=int(np.round(self.x.size/4))
           top=int(np.round(self.x.size/2))
           self._branchup=integrate.simps(self.y[0:middle],self.x[0:middle])
           self._branchdown=integrate.simps(self.y[middle:top],self.x[middle:top])
           self.result=self._branchdown-self._branchup
        else:
           middle=int(np.round(self.x.size/2))
           #self._branchup=integrate.simps(self.y[0: middle],self.x[0: middle])
           #self._branchdown=integrate.simps(self.y[middle:self.x.size],self.x[middle:self.x.size])
           self._branchdown=integrate.simps(self.y,self.x)
           self._branchup=integrate.simps(-np.flipud(self.y),-np.flipud(self.x))
           self.result=(-self._branchdown+self._branchup)/2
        return self.result

if __name__ == "__main__":
    mainDir = "W:\\Micro\\Riccardo\\Dot\\Single\\Results\\Hyst_new\\Bis"
    filename="dot_Hy_650_t25_bis.dat"
    integ=integral(filename,mainDir)
    energy=2*4*np.pi*1.e-7*integ.result
    dati=np.array([])
    dati=np.append(dati,(int(150),int(50),float(2),energy))
    dati=np.reshape(dati,(-1,4))
    print(dati)
    outputfile=filename.split(".", 1)[0]+".dat"
    outputfile="Energy_"+outputfile
    np.savetxt(outputfile,dati,fmt='%4d %4d %4.2f %12.8e',header='diametro numero concentrazione energia')
    print(energy)
