import glob, os, sys
import numpy as np
import scipy.integrate as integrate
import matplotlib.pylab as plt

class Dist:
    """
    This class load the data given a filename
    """
    def __init__(self, filename, is_avoid_zeros=True):
        # It is better to make general x,y arrays
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

class DistCollector:
    """
    this is class to collect all the filenames 
    in a dictionary of instances
    Parameters:
    ===========
    mainDir: str
        Directory containing the files
    maxLex: int, opt
        max lenght of string describing the file types to consider
        such in F64ac_freq_filetype.dat
    structure: string, opt
        the structure used in the experiment (dot,pillar,thorus)
    """
    def __init__(self, mainDir, maxLen=4, structure="dot"):  
        self._mainDir = mainDir
        # Check if the dist_type exists
        # How can we do it?
        self.dis_types = self._get_distribution_types(maxLen)
        self.diameters = self._get_diameters(maxLen)
        self.thicknesses= self._get_thicknesses(maxLen)
        print(self.dis_types)
        print(self.thicknesses)
        self.distrs = dict()
        for dis_type in self.dis_types:
            self.distrs[dis_type] = dict()
            for diameter in self.diameters:
               pattern = "%s_%s_%s_00_s??.dat" % (structure, dis_type,diameter)
               pattern = os.path.join(self._mainDir, pattern)
               filenames = sorted(glob.glob(pattern))
               print('\n'.join(filenames))
               self.distrs[dis_type][diameter] = dict()
               for filename in filenames:
                    fname = os.path.join(self._mainDir, filename)
                    thick = self._get_thickness(fname)
                    self.distrs[dis_type][diameter][thick] = Dist(fname)
    def plot(self, dis_type,diameter="*",thickness="*", loglog=False):
        """
        plot all the distributions
        just giving the type ('S', 'T', 'E', etc)
        """
        if dis_type not in self.dis_types:
            print("Type %s does not exist, please check it" % dis_type)
            return
        if diameter != "*" and (diameter not in self.diameters):
            print("Diameter %s does not exist, please check it" % diameter)
            return
        #if thickness != "*" and (thickness not in self.thicknesses):
        #    print("thickness %s does not exist, please check it" % thickness)
        #    return
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for diam in sorted(self.distrs[dis_type]):
            if (diam==diameter and diameter!="*") or diameter=="*":
                for thick in sorted(self.distrs[dis_type][diam]):
                    if (thick==thickness and thickness!="*") or thickness=="*":
                        d = self.distrs[dis_type][diam][thick]
                        lb = " d= %s nm, t= %s nm" % (diam,thick)
                        if loglog:
                            ax.loglog(d.x, d.y, 'o', label=lb)
                        else:
                            ax.plot(d.x, d.y, label=lb)
        ax.legend(numpoints=1)
        ax.grid(True)
        # Here we need to explicity say to show the plot
        plt.show()

    def _get_distribution_types(self, maxLen=4):
        """
        find the type of distributions (denoted by 'S', 'T', etc)
        looking at the last character of the filenames 
        as in dot_Hyst_100_00_s20.dat
        Parameters:
        ===========
            maxLen: int, opt
            max length of the string to be searched 
        """
        filenames = glob.glob(os.path.join(self._mainDir, "*.dat"))
        filenames = [os.path.splitext(filename)[0] for filename in filenames]
        filenames = [os.path.split(filename)[1] for filename in filenames]
        filenames = [filename.split("_", 2)[1] for filename in filenames]
        dis_types = [filename for filename in filenames if len(filename) <= maxLen]
        dis_types = set(dis_types)
        return dis_types

    def _get_diameters(self, maxLen=3):
        """
        find the diameter or maxdimension of the objecr (denoted by dimension in nanometers)
        looking at the last character of the filenames 
        as in dot_Hyst_100_00_s20.dat
        Parameters:
        ===========
            maxLen: int, opt
            max length of the string to be searched 
        """
        filenames = glob.glob(os.path.join(self._mainDir, "*.dat"))
        filenames = [os.path.splitext(filename)[0] for filename in filenames]
        filenames = [os.path.split(filename)[1] for filename in filenames]
        print('\n'.join(filenames))
        filenames = [filename.split("_",3)[2] for filename in filenames]
        diameters = [filename for filename in filenames if len(filename) <= maxLen]
        diameters = set(diameters)
        return diameters
    def _get_thicknesses(self, maxLen=3):
        """
        find the diameter or maxdimension of the objecr (denoted by dimension in nanometers)
        looking at the last character of the filenames 
        as in dot_Hyst_100_00_s20.dat
        Parameters:
        ===========
            maxLen: int, opt
            max length of the string to be searched 
        """
        filenames = glob.glob(os.path.join(self._mainDir, "*.dat"))
        filenames = [os.path.splitext(filename)[0] for filename in filenames]
        filenames = [os.path.split(filename)[1] for filename in filenames]
        print('\n'.join(filenames))
        filenames = [filename.split("_s",1)[1] for filename in filenames]
        thicknesses = [filename for filename in filenames if len(filename) <= maxLen]
        thicknesses = set(thicknesses)
        return thicknesses
    def _get_diameter(self,filename,maxLen=3):
        """
        find the diameter or maxdimension of the objecr (denoted by dimension in nanometers)
        looking at the last character of the filenames 
        as in dot_Hyst_100_00_s20.dat
        Parameters:
        ===========
            filename
            maxLen: int, opt
            max length of the string to be searched 
        """
        filename = os.path.splitext(filename)[0] 
        filename = os.path.split(filename)[1] 
        filename = filename.split("_",3)[2] 
        diameter = filename 
        return diameter

    def _get_thickness(self,filename, maxLen=3):
        """
        find the diameter or maxdimension of the objecr (denoted by dimension in nanometers)
        looking at the last character of the filenames 
        as in dot_Hyst_100_00_s20.dat
        Parameters:
        ===========
            filename
            maxLen: int, opt
            max length of the string to be searched 
        """
        filename = os.path.splitext(filename)[0] 
        filename = os.path.split(filename)[1] 
        filename = filename.split("_s")[-1] 
        thickness = filename 
        return thickness

class integral:
    """
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
        self.fullHyst=self.x[-1]+self.x[0]
    
    def avoid_zeros(self):
        is_not_zero = self.y != 0
        x = self.x[is_not_zero]
        y = self.y[is_not_zero]
        return x, y

    def integrate(self):
        if self.fullHyst==0:
           self.result=integrate.trapz(self.y,self.x)
           print(self.result,self.fullHyst,self.x[-1],self.x[1])
        else:
           self.result=integrate.trapz(self.y,self.x)
           print(self.result,self.fullHyst,self.x[-1],self.x[1])

if __name__ == "__main__":
    mainDir = "C:\\Projects\\Git\\Python-In-The-Lab_Project\\Hyst"
    dcoll = DistCollector(mainDir)
    dcoll.plot("Hyst",thickness="30")
    integ=integral("dot_Hyst_100_00_s20.dat",mainDir)
    integ.integrate()
