import glob, os, sys
import numpy as np
import scipy.integrate as integrate
import scipy.ndimage
import matplotlib.pylab as plt
from scipy.interpolate import griddata

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
        self.plotTypes=dict()
        self.plotTypes= {'Hy': 'Hysteresis Loop','Hyst': 'Hysteresis Loop', 'Ener': 'Energies'}
        self.dis_types = self._get_distribution_types(maxLen)
        self.diameters = self._get_diameters(maxLen)
        self.thicknesses= self._get_thicknesses(maxLen)
        print(self.dis_types)
        print(self.thicknesses)
        self.distrs = dict()
        for dis_type in self.dis_types:
            self.distrs[dis_type] = dict()
            for diameter in self.diameters:
               pattern = "%s_%s_%s_00_s*.dat" % (structure, dis_type,diameter)
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
        if thickness != "*" and (thickness not in self.thicknesses):
            print("thickness %s does not exist, please check it" % thickness)
            return
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('%s' % self.plotTypes[dis_type])
        if diameter != "*":
            if thickness != "*":
                ax.set_title('%s , diameter = %s nm, thickness = %s nm' % (self.plotTypes[dis_type],diameter,thickness))
            else:
                ax.set_title('%s , diameter = %s nm' % (self.plotTypes[dis_type],diameter))
            
        if (thickness != "*" and diameter == "*"):
            ax.set_title('%s , thickness = %s nm' % (self.plotTypes[dis_type],thickness))

        for diam in sorted(self.distrs[dis_type]):
            if (diam==diameter and diameter!="*") or diameter=="*":
                for thick in sorted(self.distrs[dis_type][diam]):
                    if (thick==thickness and thickness!="*") or thickness=="*":
                        d = self.distrs[dis_type][diam][thick]
                        if thickness=="*" and diameter=="*":
                            lb = " d= %s nm, t= %s nm" % (diam,thick)
                        else:
                            if diameter=="*":
                                lb = "d= %s nm" % (diam)
                            else:
                                lb = "t= %s nm" % (thick)
                        ax.plot(d.x, d.y, label=lb)
        
        ax.legend(numpoints=1,loc=4)
        ax.grid(True)
        # Here we need to explicity say to show the plot
        plt.show()

    def _get_distribution_types(self, maxLen=4):
        """
        find the type of distributions 
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
        find the diameter or maxdimension of the object (denoted by dimension in nanometers)
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
    def _get_thicknesses(self, maxLen=4):
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
        for filename in filenames:
               if "v" in filename:
                  filename = ['%s.%s' %(filename.split("v",1)[0],filename.split("v",1)[1])]
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
        if "v" in filename:
              part1=filename.split("v",1)[0]
              part2=filename.split("v",1)[1]
              filename = ''.join((filename.split("v",1)[0],'.',filename.split("v",1)[1]))
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
           self.result=-self._branchdown-self._branchup
        else:
           middle=int(np.round(self.x.size/2))
           self._branchdown=integrate.simps(self.y,self.x)
           self._branchup=integrate.simps(-np.flipud(self.y),-np.flipud(self.x))
           self.result=(-self._branchdown+self._branchup)/2
        return self.result

class mapsHystEnergy:
    """
    this is class to collect all the filenames 
    in a dictionary of instances and plot the desired map givien the parameters
    Parameters:
    ===========
    mainDir: str
        Directory containing the files
    maxLex: int, opt
        max lenght of string describing the file types to consider
        such in dot_Hyst_500_00_s30.dat
    structure: string, opt
        the structure used in the experiment (dot,pillar,thorus)
    """
    def __init__(self, mainDir,structure="dot"):
        self.dist=DistCollector(mainDir)
    def integra(self,x,y):
        self.fullHyst=x[-1]-x[0]
        if self.fullHyst==0:
           middle=int(np.round(x.size/4))
           top=int(np.round(x.size/2))
           self._branchup=integrate.simps(y[0:middle],x[0:middle])
           self._branchdown=integrate.simps(y[middle:top],x[middle:top])
           self.result=-self._branchdown-self._branchup
        else:
           middle=int(np.round(x.size/2))
           self._branchdown=integrate.simps(y,x)
           self._branchup=integrate.simps(-np.flipud(y),-np.flipud(x))
           self.result=(-self._branchdown+self._branchup)/2
        return self.result

    def setData(self,outName="mapdata",structure="dot",dis_type="Hyst"): 
        points=np.array([])    
        values = np.array([])
        mappatxt = np.array([])
        for diam in sorted(self.dist.distrs[dis_type]):
            for thick in sorted(self.dist.distrs[dis_type][diam]):
                points=np.append(points,(int(diam),float(thick)))
                value=self.integra(self.dist.distrs[dis_type][diam][thick].x,self.dist.distrs[dis_type][diam][thick].y)
                self.energy=2*4*np.pi*1.e-7*value
                values=np.append(values,self.energy)
                print(self.energy,diam,thick)
                mappatxt=np.append(mappatxt,(int(diam),float(thick),self.energy))
        mappatxt=np.reshape(mappatxt,(-1,3))
        points=np.reshape(points,(-1,2))
        values=np.reshape(values,(-1,1))
        np.savetxt(outName,mappatxt[:],"%4d  %4.2f %12.8e")
        return (points,values)

    def plotMap(self):
        points,values=self.setData()
        #xmin=np.min(points[:,0])
        #xmax=np.max(points[:,0])
        #ymin=np.min(points[:,1])
        #ymax=np.max(points[:,1])
        
        grid_x, grid_y = np.mgrid[np.min(points[:,0]):np.max(points[:,0]):100j, np.min(points[:,1]):np.max(points[:,1]):100j]
        #print(grid_x, grid_y)
        
        grid_z0 = griddata((points[:,0],points[:,1]), values, (grid_x, grid_y), method='cubic',fill_value=np.min(values)/2)
        print(np.min(values)/2)
        #
        origin = 'lower'
        CS=plt.contourf(grid_x,grid_y,grid_z0[:,:,0],100)
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        CS2 = plt.contour(CS, levels=CS.levels[::10],
                          colors='k',
                          origin=origin,
                          hold='on')
        plt.clabel(CS2, fontsize=9, inline=1)
        #plt.axis([200, 650, 10, 30])
        plt.colorbar(CS)
        plt.show()

if __name__ == "__main__":
    mainDir = "C:\\Projects\\Git\\Python-In-The-Lab_Project\\Hyst"
    #mainDir = "D:\\git\\Python-In-The-Lab_Project\\Python-In-The-Lab_Project\\Hyst"


    dcoll = DistCollector(mainDir)
    dcoll.plot("Hyst",thickness="20")
    integ=integral("dot_Hyst_500_00_s30.dat",mainDir)
    
    maps=mapsHystEnergy(mainDir)
    maps.plotMap()
    
  
    #print(dcoll.distrs["Hyst"]["300"]["30"].x)
    #print(integ.energy)

