import glob, os, sys
import h5py
import numpy as np
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



"""
Basic script Open a HDF5 file of my simulation and compute the Hysteresis loop, saves data in an opportune file with specific naming pattern
at the end plots the calculated loop.
"""


class MagnetizationCalc:
    """
    this is class to load HDF5 file and compute the time behaviour of mangetization or the hysteresis cycle

    Parameters:
    ===========
    mainDir: str
        Directory containing the files
    filename: str
        name of the file
    maxLex: int, opt
        max lenght of string describing the file types to consider
        such in F64ac_freq_filetype.dat
    hysteresis: bool, opt
        compute hysteresis loop or time evolution (hyst = true (def),  dt=1 (def choice) (false time evolution) dt=0 read dt from file dt= xxx set a specific dt))
    versoreu = np.array([[1],[0],[0]]), opt
    versorev = np.array([[0],[1],[0]]), opt
    versorew = np.array([[0],[0],[1]]), opt
        direction of the applied field
    """

    def __init__(self, mainDir, filename):
        self._mainDir = mainDir
        self._filename = filename

        ## If you want, you can avoid the creation of 3 subdic
        ## by using a tuple as key
        ## (dis_type, diameter, thick)
        self.outputplot = filename.split(".", 1)[0] + ".pdf"
        self.outputplot = self.outputplot.split("_", 1)[0] + "_Hyst_" + self.outputplot.split("_", 1)[1]
        self.outputfile = filename.split(".", 1)[0] + ".dat"


        print(self.outputfile)
        self.hdf5_file_name = os.path.join(mainDir, filename)

        self.dataset_numTimeSteps = '/TimestepsNumber'

        if not os.path.isfile(self.hdf5_file_name):
            print("%s file do not exists" % (self.hdf5_file_name))
            self.x, self.y = [0, 0]
        else:
            self.file = h5py.File(self.hdf5_file_name, 'r')  # 'r' means that hdf5 file is open in read-only mode

            self.equilibria = [name.split('Emme', 1)[1] for name in self.file if 'Emme' in name]
            self.equilibria = [int(i) for i in self.equilibria]

            datasetTime = self.file[self.dataset_numTimeSteps]
            # datasetVol=file[dataset_Volumes]
            numTimeSteps = datasetTime[(0)]
            print(numTimeSteps)

    def computeData(self, hysteresis=True, dt=1, versoreu = np.array([[1],[0],[0]]), versorev = np.array([[0],[1],[0]]), versorew = np.array([[0],[0],[1]])):
        self.outputdata = np.array([])
        if hysteresis:
            for equilibrium in sorted(self.equilibria):
                self.outputdata = np.append(self.outputdata, calcoloMagnMediaVsappField(equilibrium, self.file, versoreu, versorev, versorew))

            print(np.shape(self.outputdata), "np.shape outputdata")
            self.outputdata = np.reshape(self.outputdata, (-1, 6))
            self.outputfile = self.outputfile.split("_", 1)[0] + "_Hyst_" + self.outputfile.split("_", 1)[1]
            np.savetxt(os.path.join(self._mainDir, self.outputfile), self.outputdata, fmt='%26.18e')
        else:
            for equilibrium in sorted(self.equilibria):
                self.outputdata = np.append(self.outputdata, calcoloMagnMedia(equilibrium, self.file, versoreu, versorev, versorew,dt))

            print(np.shape(self.outputdata), "np.shape outputdata")
            self.outputdata = np.reshape(self.outputdata, (-1, 4))
            self.outputfile = self.outputfile.split("_", 1)[0] + "_timeSer_" + self.outputfile.split("_", 1)[1]
            np.savetxt(os.path.join(self._mainDir, self.outputfile), self.outputdata, fmt='%26.18e')

    def plotData(self, hysteresis=True, versoreu=np.array([[1], [0], [0]]), dt=1, versorev=np.array([[0], [1], [0]]), versorew=np.array([[0], [0], [1]])):
        #interamente da scrivere
        self.outputdata = np.array([])
        if hysteresis:
            print('hysteresis plot')
        else:
            print('time plot')



def calcoloMagnMediaVsappField(time, file, versoreu, versorev, versorew):
    data = np.array([])
    dataset_Magnet = '/Emme%s/Val' % (time)
    dataset_Hext = '/Hext%s/Val' % (time)
    # print(dataset_Magnet)
    datasetM = file[dataset_Magnet]
    # print(datasetM.shape, isinstance(datasetM,h5py.Dataset))
    # magnetizzazione  = np.matrix(datasetM[0:103,:])
    magnetizzazione = np.matrix(datasetM[()])

    # print(np.shape(magnetizzazione))
    proiezu = np.dot(magnetizzazione, versoreu)
    proiezv = np.dot(magnetizzazione, versorev)
    proiezw = np.dot(magnetizzazione, versorew)
    # print(proiezw,i, "\n")
    datasetH = file[dataset_Hext]
    # print(datasetH.shape, isinstance(datasetH,h5py.Dataset))
    # Hext= datasetH[0:103,0]
    Hext = datasetH[(0)]
    Hext = np.dot(np.dot(Hext, versoreu), np.reshape((1, 0, 0), (1, 3))) + np.dot(np.dot(Hext, versorev),
                                                                                  np.reshape((0, 1, 0),
                                                                                             (1, 3))) + np.dot(
        np.dot(Hext, versorew), np.reshape((0, 0, 1), (1, 3)))

    Volumes = np.ones(proiezu.shape[0]) * (5.e-9 * 5.e-9 * 5.e-9)
    mediau = np.average(proiezu, axis=0, weights=Volumes)
    mediav = np.average(proiezv, axis=0, weights=Volumes)
    mediaw = np.average(proiezw, axis=0, weights=Volumes)
    data = np.append(data, [Hext[0], mediau, Hext[1], mediav, Hext[2], mediaw])
    return data
def calcoloMagnMedia(time, file, versoreu, versorev, versorew,dt=1):
    data = np.array([])
    dataset_Magnet = '/Emme%s/Val' % (time)
    # print(dataset_Magnet)
    datasetM = file[dataset_Magnet]
    # print(datasetM.shape, isinstance(datasetM,h5py.Dataset))
    # magnetizzazione  = np.matrix(datasetM[0:103,:])
    magnetizzazione = np.matrix(datasetM[()],dtype=np.float64)

    proiezu = np.dot(magnetizzazione, np.float64(versoreu))
    proiezv = np.dot(magnetizzazione, np.float64(versorev))
    proiezw = np.dot(magnetizzazione, np.float64(versorew))
    # print(proiezw,i, "\n")
    if dt==0:
        dataset_timestamp = '/Timestamps'
        datasetT = file[dataset_timestamp]
        timestamp=datasetT[(time-1)]
    else:
        timestamp=dt*(time-1)
    Volumes = np.ones(proiezu.shape[0]) * (5.e-9 * 5.e-9 * 5.e-9)
    mediau = np.average(proiezu, axis=0, weights=Volumes)
    mediav = np.average(proiezv, axis=0, weights=Volumes)
    mediaw = np.average(proiezw, axis=0, weights=Volumes)
    data = np.append(data,[timestamp, mediau,  mediav,  mediaw])
    return data

if __name__ == '__main__':
    import math
    #mainDir = "C:\\Projects\\Sally_adaptive_test_case"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\dot\\100\\t30"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Square\\200\\45\\parallel"
    #mainDir = "W:\\Micro\\Riccardo\\cfr2d3d_3d_random\\3d"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Sphere\\100"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Cube\\50"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\dot\\timeevolution\\preview"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\dot\\150\\Angles"
    #mainDir ="W:\\Micro\\Riccardo\\3D\\Article3D\\Sally3D\\20nm\\square\\50nm"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Article3D\\Sally3D\\sigma\\sph100nm\\review"
    #mainDir="C:\\Riccardo\\workingfolder_article3d\\sq50nm\\t20"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Article3D\\MuMag4_new\\1nm"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Article3D\\Sally3D\\oscillator\\newtesting\\sm"
    mainDir = "W:\\Micro\\Riccardo\\3D\\Pallozzi"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Tubitak_Fe3O4"
    #mainDir = "Q:\\Riccardo\\newBlob2"
    #extensions=["TIM", "h5", "xmf", "MAT", "UTL", "SLZ", "GEO", "EMI","inp"]
    #for i in range(33,35):
    #    name='inp'+str(i)
    #    f = open(os.path.join(mainDir, name+'.inp'), "r")
    #    caseName=f.readlines()[3].split(".", 1)[0]
    #    f.close()
    #    for extension in extensions:
    #        try:
    #            os.rename(os.path.join(mainDir, name+'.'+extension),os.path.join(mainDir, caseName+'.'+extension))
    #        except :
    #            pass
    #    print(caseName)
    #    fileData = caseName+".h5"
    #    #v1=np.array([[math.cos(math.pi/12)], [math.sin(math.pi/12)], [0]])
    #    #v2=np.array([[-math.sin(math.pi/12)], [math.cos(math.pi/12)], [0]])
    #    #v3=np.array([[0], [0], [1]])
    #    data = MagnetizationCalc(mainDir,fileData)
    #    data.computeData(hysteresis=True)
    #    data.file.close()
    #os.rename(r'file path\OLD file name.file type',r'file path\NEW file name.file type')
    filename = "bl_a025c022h025fzD.h5"
    #v1=np.array([[math.cos(math.pi/12)], [math.sin(math.pi/12)], [0]])
    #v2=np.array([[-math.sin(math.pi/12)], [math.cos(math.pi/12)], [0]])
    #v3=np.array([[0], [0], [1]])
    data = MagnetizationCalc(mainDir,filename)
    #data.computeData(hysteresis=True,dt=1,versoreu=v1,versorev=v2,versorew=v3)
    data.computeData(hysteresis=True)
    #data.computeData( hysteresis = False, dt=1.e-13)
    #data.computeData()
    data.file.close()
    #filename = "sq50_t20s2v5_1e-4_2.h5"
    #data = MagnetizationCalc(mainDir, filename)
    #data.computeData(hysteresis=False, dt=0.2e-11)
    ## data.computeData()
    #data.file.close()

    #filename = "sq50_t20s1v25_1e-4.h5"
    #data = MagnetizationCalc(mainDir, filename)
    # data.computeData(False,dt=0.2e-11)
    #data.computeData()
    #data.file.close()
    # outputplot= filename.split(".", 1)[0] + ".pdf"
    # outputplot = outputplot.split("_", 1)[0] + "_Hyst_" + outputplot.split("_", 1)[1]
    # outputfile = filename.split(".", 1)[0] + ".dat"
    # outputfile = outputfile.split("_", 1)[0] + "_Hyst_" + outputfile.split("_", 1)[1]
    #
    # print(outputfile)
    # hdf5_file_name = os.path.join(mainDir, filename)
    #
    # dataset_numTimeSteps = '/TimestepsNumber'
    # # dataset_Volumes ='/Volumes'
    # event_number = 5
    #
    # versoreu = np.array([[1],[0],[0]])
    # versorev = np.array([[0],[1],[0]])
    # versorew = np.array([[0],[0],[1]])
    # # versoreT=np.reshape(versore,(1,3))
    # file = h5py.File(hdf5_file_name, 'r')  # 'r' means that hdf5 file is open in read-only mode
    #
    #
    # equilibria = [name.split('Emme',1)[1] for name in file if 'Emme' in name]
    # equilibria = [int(i) for i in equilibria]
    #
    # datasetTime = file[dataset_numTimeSteps]
    # # datasetVol=file[dataset_Volumes]
    # numTimeSteps = datasetTime[(0)]
    # print(numTimeSteps)
    # mediau = np.array([])
    # mediav = np.array([])
    # mediaw = np.array([])
    # Hexternal = np.array([])
    # outputdata = np.array([])
    # # Volumes=np.array(datasetVol[()])
    #
    # for equilibrium in sorted(equilibria):
    #     outputdata = np.append(outputdata, calcoloMagnMediaVsappField(equilibrium, file, versoreu, versorev, versorew))
    #
    # print(np.shape(outputdata), "np.shape outputdata")
    # outputdata = np.reshape(outputdata, (-1, 6))
    # np.savetxt(os.path.join(mainDir, outputfile), outputdata, fmt='%26.18e')
    #
    # file.close()
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # lb = "u"
    # ax.plot(outputdata[1:-1, 0]/1000, outputdata[1:-1, 1]/1000, label=lb)
    # lb = "v"
    # ax.plot(outputdata[1:-1, 2]/1000, outputdata[1:-1, 3]/1000, label=lb)
    # lb = "w"
    # ax.plot(outputdata[1:-1, 4]/1000, outputdata[1:-1, 5]/1000, label=lb)
    # ax.legend(numpoints=1)
    # ax.grid(True)
    #
    # ax.ticklabel_format(axis='both', style='sci', scilimits=(-2, 2),useMathText=True)
    # #fmt = matplotlib.ticker.StrMethodFormatter("{x:2.2e}")
    #
    # #ax.xaxis.set_major_formatter(fmt)
    # #ax.yaxis.set_major_formatter(fmt)
    #
    # ax.set_xlabel('\\textbf{Applied field} (kA/m)')
    # ax.set_ylabel('\\textbf{Magnetization} (kA/m)')
    # #ax.set_title(r'\TeX\ is Number $\displaystyle\sum_{n=1}^\infty \frac{-e^{i\pi}}{2^n}$!', color='r')
    # #fig.text(0.5, 1.01 ,r'\TeX\ is Number $\displaystyle\sum_{n=1}^\infty'
    # #             r'\frac{-e^{i\pi}}{2^n}$!', color='r', horizontalalignment='center',transform = ax.transAxes)
    # fig.text(0.5, 1.0, r'Hysteresis loop for permalloy squares of d=200 nm', color='r', horizontalalignment='center',transform = ax.transAxes)
    # plt.tight_layout()
    # #plt.subplots_adjust(top=0.995)
    # plt.legend(loc='best')
    # # plt.plot(Hexternal, mediau)
    #
    # plt.savefig(os.path.join(mainDir, outputplot), bbox_inches='tight', transparent=True,)
    # plt.show()
    # #
