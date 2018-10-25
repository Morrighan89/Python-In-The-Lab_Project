import glob, os, sys
import numpy as np
import scipy.integrate as integrate
import scipy.ndimage
import matplotlib.pylab as plt
from scipy.interpolate import griddata

def integra(x,y,method='simps'):
        fullHyst = x[-1] == x[0]
        if fullHyst:
           middle=int(np.round(x.size/2))
           top=int(np.round(x.size))
           if method=='simps':
               branchup=integrate.simps(y[0:middle],x[0:middle])
               branchdown=integrate.simps(y[middle:top],x[middle:top])
           else:
               branchup=integrate.trapz(y[0:middle],x[0:middle])
               branchdown=integrate.trapz(y[middle:top],x[middle:top])   
           result=(-branchdown-branchup)/2
        else:
            if method=='simps':
                branchdown=integrate.simps(y,x)
                branchup=integrate.simps(-np.flipud(y),-np.flipud(x))
            else:
                branchdown=integrate.trapz(y,x)
                branchup=integrate.trapz(-np.flipud(y),-np.flipud(x))
            result=(-branchdown+branchup)/2
        return result

class Dist:
    """
    This class load the data given a filename
    and gives the possibility to generate a plot with the uploaded data
    """
    def __init__(self, filename, is_avoid_zeros=True):
        # It is better to make general x,y arrays
        
        if not os.path.isfile(filename):
            filename='%s %s' %(filename.split(".dat",1)[0],".DAT")
            if not os.path.isfile(filename):
                print("%s file do not exists" % (filename))
                self.x, self.y=[0,0]
            else:
                self.x, self.y = np.loadtxt(filename, comments="#", unpack=True)
                if is_avoid_zeros:
                    s_len = len(self.x)
                    self.x, self.y = self.avoid_zeros()
                    print("%i lines deleted" % (s_len - len(self.x)))
        else:
            self.x, self.y = np.loadtxt(filename, comments="#", unpack=True)
            if is_avoid_zeros:
                s_len = len(self.x)
                self.x, self.y = self.avoid_zeros()
                print("%i lines deleted" % (s_len - len(self.x)))
        
    
    def avoid_zeros(self):
        is_not_zero = self.y != 0
        x = self.x[is_not_zero]
        y = self.y[is_not_zero]
        return x, y

    def plot(self, loglog=True):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        if loglog:
            ax.loglog(self.x, self.y, 'o')
        else:
            ax.plot(self.x, self.y, 'o')

class Integral:
    """
    Standalone version of integrate class
    This class load the data given a filename and integrates the curve
    """
    def __init__(self, filename, mainDir, is_avoid_zeros=True):
        self._mainDir = mainDir
        fname = os.path.join(self._mainDir, filename)
        self.dist=Dist(fname,is_avoid_zeros)
        # It is better to make general x,y arrays        
        value=integra( self.dist.x,  self.dist.y)
        self.energy=2*4*np.pi*1.e-7*value

if __name__ == "__main__":
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Mumax_dot_pillars"
    mainDir = "W:\\Micro\\Riccardo\\3D\\ring\\150"
    #mainDir = "W:\\Micro\\2d3d\\dot680\\Hysteresis"
    filename = "ring_Hyst_150w03t30.txt"
    integ=Integral(filename,mainDir)
    dati=np.array([])
    dati=np.append(dati,(int(150),int(40),integ.energy))
    dati=np.reshape(dati,(-1,3))
    print(dati)
    outputfile=filename.split(".", 1)[0]+".dat"
    outputfile="Energy_"+outputfile
    np.savetxt(os.path.join(mainDir, outputfile),dati,fmt='%4d %4d  %12.8e',header='diametro spessore energia')
    print(integ.energy)
