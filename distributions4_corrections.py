import glob, os, sys
import numpy as np
import scipy.integrate as integrate
import scipy.ndimage
import matplotlib.pylab as pltt
from scipy.interpolate import griddata
import matplotlib
from matplotlib.backends.backend_pgf import FigureCanvasPgf
matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)

import matplotlib.pyplot as plt

pgf_with_custom_preamble = {
    "pgf.texsystem": "lualatex",
    "font.family": "serif",  # use serif/main font for text elements
    "text.usetex": True,     # use inline math for ticks
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "axes.labelsize": 16,
    "font.size": 18,
    "legend.fontsize": 16,
    "axes.titlesize": 16,           # Title size when one figure
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "figure.titlesize": 18,         # Overall figure title
    "pgf.preamble": [
         r'\usepackage{fontspec}',
         r'\usepackage{units}',          # load additional packages
         r'\usepackage{metalogo}',
         r'\usepackage{unicode-math}',   # unicode math setup
         r'\setmathfont{XITS Math}',
         r'\setmonofont{Libertinus Mono}'
         r'\setmainfont{Libertinus Serif}',  # serif font via preamble
         ]
}
matplotlib.rcParams.update(pgf_with_custom_preamble)


def integra(x, y, method='simps'):
    fullHyst = x[-1] == x[0]
    if fullHyst:
        middle = int(np.round(x.size / 2))
        top = int(np.round(x.size))
        if method == 'simps':
            branchup = integrate.simps(y[0:middle], x[0:middle])
            branchdown = integrate.simps(y[middle:top], x[middle:top])
        else:
            branchup = integrate.trapz(y[0:middle], x[0:middle])
            branchdown = integrate.trapz(y[middle:top], x[middle:top])
        result = (-branchdown - branchup) / 2
    else:
        if method == 'simps':
            branchdown = integrate.simps(y, x)
            branchup = integrate.simps(-np.flipud(y), -np.flipud(x))
        else:
            branchdown = integrate.trapz(y, x)
            branchup = integrate.trapz(-np.flipud(y), -np.flipud(x))
        result = (-branchdown + branchup) / 2
    return result

def integraHalf(x, y, method='simps'):
    fullHyst = x[-1] == x[0]
    if fullHyst:
        quarter = int(np.round(x.size / 4))
        triquarter = int(np.round(x.size))-int(np.round(x.size / 4))
        if method == 'simps':
            branchup = integrate.simps(y[0:quarter], x[0:quarter])
            branchdown = integrate.simps(y[triquarter:-1], x[triquarter:-1])
        else:
            branchup = integrate.trapz(y[0:quarter], x[0:quarter])
            branchdown = integrate.trapz(y[triquarter:-1], x[triquarter:-1])
        result = (branchdown,branchup)
    else:
        half = int(np.round(x.size / 2))
        if method == 'simps':
            branchdown = integrate.simps(y[0:half], x[0:half])
            branchup = integrate.simps(y[half:-1], x[half:-1])
        else:
            branchdown = integrate.trapz(y[0:half], x[0:half])
            branchup = integrate.trapz(y[half:-1], x[half:-1])
            result = (branchdown, branchup)
    return (branchdown, branchup)
def integra2Half(x, y, method='simps'):
    fullHyst = x[-1] == x[0]
    if fullHyst:
        quarter = int(np.round(x.size / 4))
        middle = int(np.round(x.size / 2))
        triquarter = int(np.round(x.size))-int(np.round(x.size / 4))
        if method == 'simps':
            branchup = integrate.simps(y[quarter:middle], x[quarter:middle])
            branchdown = integrate.simps(y[middle:triquarter], x[middle:triquarter])
        else:
            branchup = integrate.trapz(y[quarter:middle], x[quarter:middle])
            branchdown = integrate.trapz(y[middle:triquarter], x[middle:triquarter])
        result = (branchdown,branchup)
    else:
        half = int(np.round(x.size / 2))
        if method == 'simps':
            branchdown = integrate.simps(y[0:half], x[0:half])
            branchup = integrate.simps(y[half:-1], x[half:-1])
        else:
            branchdown = integrate.trapz(y[0:half], x[0:half])
            branchup = integrate.trapz(y[half:-1], x[half:-1])
            result = (branchdown, branchup)
    return (branchdown, branchup)


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

class DistCollector:
    """
    this is class to collects all the filenames 
    in a dictionary of instances and allows to produce different plots
    selecting four main parameters.
    First the type of structure. Subsequently for the given nanostructure it is possible to select the quantity or type of distribution to plot,
    and restrict the analysis to a given diameter or thickness.
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

        self.plotTypes= {'Hy': 'Hysteresis Loop','Hyst': 'Hysteresis Loop', 'Ener': 'Energies'}
        self._get_parameters()
        print(self.dis_types)
        print(self.thicknesses)

        ## If you want, you can avoid the creation of 3 subdic
        ## by using a tuple as key
        ## (dis_type, diameter, thick)
        self.distrs = dict()
        for dis_type in self.dis_types:
            self.distrs[dis_type] = dict()
            for diameter in self.diameters:
               pattern = "%s_%s_%s_t*.dat" % (structure, dis_type,diameter)
               pattern = os.path.join(self._mainDir, pattern)
               filenames = sorted(glob.glob(pattern))
               print('\n'.join(filenames))
               self.distrs[dis_type][diameter] = dict()
               for filename in filenames:
                    fname = os.path.join(self._mainDir, filename)
                    thick = self._get_thickness(fname)
                    self.distrs[dis_type][diameter][thick] = Dist(fname)
               #print( self.distrs["Hyst"]["150"]["75"])
                    
    def plot(self, dis_type,diameter="*",thickness="*", loglog=False):
        """
        plot all the distributions with the possibility to restrict to a specific diameter or thickness or type
        
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

    def _get_parameters(self, pattern=".dat", n_elements=4):
        filenames = glob.glob1(self._mainDir, "*")
        filenames = [os.path.splitext(filename)[0] for filename in filenames if pattern.upper() in filename.upper()]
        q = np.concatenate([np.array(filename.split("_")[:n_elements]) for filename in filenames]).flatten()
        q = q.reshape(-1,n_elements)
        self.dis_types = set(q[:,1])
        self.diameters = set(q[:,2])
        thicknesses = set(q[:,3])
        thicknesses=[thickness.split("t",1)[1] for thickness in thicknesses]
        thicknesses=[ '%s.%s' %(thickness.split("v",1)[0],thickness.split("v",1)[1]) if "v" in thickness else  thickness for thickness in thicknesses]     
        self.thicknesses=thicknesses
        # Here you can add your test (maxLen, etc)



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
        filename = filename.split("_t")[-1]
        if "v" in filename:
              part1=filename.split("v",1)[0]
              part2=filename.split("v",1)[1]
              filename = ''.join((filename.split("v",1)[0],'.',filename.split("v",1)[1]))
        thickness = filename 
        return thickness

class Integral:
    """
    This class load the data given a filename and integrates the curve
    """
    def __init__(self, filename, mainDir, is_avoid_zeros=True):
        self._mainDir = mainDir
        fname = os.path.join(self._mainDir, filename)
        self.dist=Dist(fname,is_avoid_zeros)
        # It is better to make general x,y arrays        
        value=integra( self.dist.x,  self.dist.y)
        self.energy=2*4*np.pi*1.e-7*value


class MapsHystEnergy:
    """
    this is class to cuses the Dist Collector class to read and analyze the file in the given folder
    Integrates the different hysteresys loops and generates a color map of the specific energy (J/m^3) due to hysteresis losses
    On the x axes we have the length of the diameter or major axe of the magnetic nanostructure (nm)
    On the y axes we have the thickness of the magnetic nanostructure
    Parameters:
    ===========
    mainDir: str
        Directory containing the files
    structure: string, opt
        the structure used in the experiment (dot,pillar,thorus,rings)
    ===========
    integra:
        given the x,y arrays evaluates the area of the Hysteresis loop
    setData:
        uses the data read from the dist collector routine and the dictionary
        and calling the function integra generates the data for the color map
        and saves them on a file "mapdata"
    plotmap:
        interpolates the data generated by setData and plots a nice and smooth "heatmap"
    """
    def __init__(self, mainDir,structure="dot"):
        self.dist=DistCollector(mainDir)


    def setData(self,outName="mapdata",structure="dot",dis_type="Hyst"): 
        points=np.array([])    
        values = np.array([])
        mappatxt = np.array([])
        for diam in sorted(self.dist.distrs[dis_type]):
            for thick in sorted(self.dist.distrs[dis_type][diam]):
                points=np.append(points,(int(diam),float(thick)))
                value=integra(self.dist.distrs[dis_type][diam][thick].x,self.dist.distrs[dis_type][diam][thick].y)
                (branchdown, branchup)=integraHalf(self.dist.distrs[dis_type][diam][thick].x,self.dist.distrs[dis_type][diam][thick].y)
                self.energy=2*4*np.pi*1.e-7*value
                self.branchdown=4*np.pi*1.e-7*branchdown
                self.branchup = 4 * np.pi * 1.e-7 * branchup
                (branchdown, branchup) = integra2Half(self.dist.distrs[dis_type][diam][thick].x,self.dist.distrs[dis_type][diam][thick].y)
                self.branchdown2 = 4 * np.pi * 1.e-7 * branchdown
                self.branchup2 = 4 * np.pi * 1.e-7 * branchup
                values=np.append(values,self.energy)
                print(self.energy,diam,thick)
                mappatxt=np.append(mappatxt,(int(diam),float(thick),self.energy,self.branchup,self.branchdown,self.branchup2,self.branchdown2))
        mappatxt=np.reshape(mappatxt,(-1,7))
        points=np.reshape(points,(-1,2))
        values=np.reshape(values,(-1,1))
        np.savetxt(os.path.join(mainDir, outName),mappatxt[:],"%4d  %4.2f %14.10e  %14.10E  %14.10e %14.10e %14.10e")
        return (points,values)

    def plotMap(self):
        points,values=self.setData()
        grid_x, grid_y = np.mgrid[np.min(points[:,0]):np.max(points[:,0]):100j, np.min(points[:,1]):np.max(points[:,1]):100j]
        fill=(np.min(values)/2)
        grid_z0 = griddata((points[:,0],points[:,1]), values, (grid_x, grid_y), method='linear',fill_value=np.nan)
        #
        origin = 'lower'
        CS=plt.contourf(grid_x,grid_y,grid_z0[:,:,0],100)
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        CS2 = plt.contour(CS, levels=CS.levels[::10],
                          colors='k',
                          origin=origin,
                          hold='on')
        plt.clabel(CS2, fontsize=9, inline=1)
        plt.colorbar(CS)
        plt.show()

if __name__ == "__main__":
    #mainDir = "C:\\Projects\\Git\\Python-In-The-Lab_Project\\Hyst"
    mainDir = "W:\\Micro\\Riccardo\\3D\\Mumax_dot_pillars"
    #mainDir = "/home/gf/src/Python/Python-in-the-lab/students/G4/Riccardo.Ferrero/Python-In-The-Lab_Project-master/Hyst"

    dcoll = DistCollector(mainDir)
    dcoll.plot("Hyst",thickness="30")
    #integ=Integral("dot_Hyst_500_00_s30.dat",mainDir)
    maps=MapsHystEnergy(mainDir)
    maps.setData()
    #maps.plotMap()
    #print(integ.energy)

##################################################################################################
##############################   OLD CODE   ######################################################
##################################################################################################

#   def _get_distribution_types(self,pattern=".dat", maxLen=4):
#       """
#       find the type of distributions in the given directory, reading the 2nd position in the files name
#       and returns all the availble diameters as in dot_Hyst_100_00_s20.dat
#       Parameters:
#       ===========
#           maxLen: int, opt
#           max length of the string to be searched 
#       """
#       filenames = glob.glob1(self._mainDir, "*")
#       filenames = [os.path.splitext(filename)[0] for filename in filenames if pattern.upper() in filename.upper()]
#       filenames = [os.path.split(filename)[1] for filename in filenames]
#       filenames = [filename.split("_", 2)[1] for filename in filenames]
#       dis_types = [filename for filename in filenames if len(filename) <= maxLen]
#       dis_types = set(dis_types)
#       return dis_types
#
#   def _get_diameters(self, maxLen=3):
#       """
#       find the diameter or maxdimension of the object (denoted by dimension in nanometers)
#       in the given directory, reading the 3rd position in the file names and returns all the availble diameters
#       as in dot_Hyst_100_00_s20.dat
#       Parameters:
#       ===========
#           maxLen: int, opt
#           max length of the string to be searched 
#       """
#       filenames = glob.glob(os.path.join(self._mainDir, "*.DAT"))
#       filenames = [os.path.splitext(filename)[0] for filename in filenames]
#       filenames = [os.path.split(filename)[1] for filename in filenames]
#       print('\n'.join(filenames))
#       filenames = [filename.split("_",3)[2] for filename in filenames]
#       diameters = [filename for filename in filenames if len(filename) <= maxLen]
#       diameters = set(diameters)
#       return diameters
#   def _get_thicknesses(self, maxLen=4):
#       """
#       find the thickness of a collection of object in the given directory,
#       reading the 5th position in the file names and returns all the availble thicknesses
#       as in dot_Hyst_100_00_s20.dat
#       Parameters:
#       ===========
#           maxLen: int, opt
#           max length of the string to be searched 
#       """
#       filenames = glob.glob(os.path.join(self._mainDir, "*.DAT"))
#       filenames = [os.path.splitext(filename)[0] for filename in filenames]
#       filenames = [os.path.split(filename)[1] for filename in filenames]
#       print('\n'.join(filenames))
#       filenames = [filename.split("_s",1)[1] for filename in filenames]
#       for filename in filenames:
#              if "v" in filename:
#                 filename = ['%s.%s' %(filename.split("v",1)[0],filename.split("v",1)[1])]
#       thicknesses = [filename for filename in filenames if len(filename) <= maxLen]
#       thicknesses = set(thicknesses)
#       return thicknesses
#   def _get_diameter(self,filename,maxLen=3):
#       """
#       find the diameter or maxdimension of the object (denoted by dimension in nanometers)
#       looking at the third position in the file name
#       as in dot_Hyst_100_00_s20.dat
#       Parameters:
#       ===========
#           filename
#           maxLen: int, opt
#           max length of the string to be searched 
#       """
#       filename = os.path.splitext(filename)[0] 
#       filename = os.path.split(filename)[1] 
#       filename = filename.split("_",3)[2] 
#       diameter = filename 
#       return diameter
#