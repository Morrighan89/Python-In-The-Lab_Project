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
    np.savetxt("uffa", proiezu)
    # print(Hext)
    Volumes = np.ones(proiezu.shape[0]) * (5.e-9 * 5.e-9 * 5.e-9)
    mediau = np.average(proiezu, axis=0, weights=Volumes)
    mediav = np.average(proiezv, axis=0, weights=Volumes)
    mediaw = np.average(proiezw, axis=0, weights=Volumes)
    data = np.append(data, [Hext[0], mediau, Hext[1], mediav, Hext[2], mediaw])
    return data
def calcoloMagnMedia(time, file, versoreu, versorev, versorew):
    data = np.array([])
    dataset_Magnet = '/Emme%s/Val' % (time)
    dataset_Hext = '/Hext%s/Val' % (time)
    # print(dataset_Magnet)
    datasetM = file[dataset_Magnet]
    # print(datasetM.shape, isinstance(datasetM,h5py.Dataset))
    # magnetizzazione  = np.matrix(datasetM[0:103,:])
    magnetizzazione = np.matrix(datasetM[()])

    # print(np.shape(magnetizzazione))
    summa=np.sum(magnetizzazione, axis=0)
    # print(proiezw,i, "\n")
    datasetH = file[dataset_Hext]
    # print(datasetH.shape, isinstance(datasetH,h5py.Dataset))
    # Hext= datasetH[0:103,0]
    Hext = datasetH[(0)]
    Hext = np.dot(np.dot(Hext, versoreu), np.reshape((1, 0, 0), (1, 3))) + np.dot(np.dot(Hext, [[1], [0], [0]]),
                                                                                  np.reshape((0, 1, 0),
                                                                                             (1, 3))) + np.dot(
        np.dot(Hext, [[1], [0], [0]]), np.reshape((0, 0, 1), (1, 3)))

    data = np.append(data, [Hext[0], summa[0,0], Hext[1], summa[0,1], Hext[2], summa[0,2]])
    return data


if __name__ == '__main__':
    #mainDir = "C:\\Projects\\Sally_adaptive_test_case"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\dot\\100\\t30"
    mainDir = "W:\\Micro\\Riccardo\\3D\\Square\\200\\45\\tilted\\preview"
    #mainDir = "W:\\Micro\\Riccardo\\cfr2d3d_3d_random\\3d"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Sphere\\100"

    filename = "sq_200_t15_45til_fine2.h5"
    outputplot= filename.split(".", 1)[0] + ".pdf"
    outputplot = outputplot.split("_", 1)[0] + "_Hyst_" + outputplot.split("_", 1)[1]
    outputfile = filename.split(".", 1)[0] + ".dat"
    outputfile = outputfile.split("_", 1)[0] + "_Hyst_" + outputfile.split("_", 1)[1]

    print(outputfile)
    hdf5_file_name = os.path.join(mainDir, filename)

    dataset_numTimeSteps = '/TimestepsNumber'
    # dataset_Volumes ='/Volumes'
    event_number = 5

    versoreu = np.array([[1],[0],[0]])
    versorev = np.array([[0], [1], [0]])
    versorew = np.array([[0],[0],[1]])
    # versoreT=np.reshape(versore,(1,3))
    file = h5py.File(hdf5_file_name, 'r')  # 'r' means that hdf5 file is open in read-only mode


    equilibria = [name.split('Emme',1)[1] for name in file if 'Emme' in name]
    equilibria = [int(i) for i in equilibria]

    datasetTime = file[dataset_numTimeSteps]
    # datasetVol=file[dataset_Volumes]
    numTimeSteps = datasetTime[(0)]
    print(numTimeSteps)
    mediau = np.array([])
    mediav = np.array([])
    mediaw = np.array([])
    Hexternal = np.array([])
    outputdata = np.array([])
    # Volumes=np.array(datasetVol[()])

    for equilibrium in sorted(equilibria):
        outputdata = np.append(outputdata, calcoloMagnMediaVsappField(equilibrium, file, versoreu, versorev, versorew))

    print(np.shape(outputdata), "np.shape outputdata")
    outputdata = np.reshape(outputdata, (-1, 6))
    np.savetxt(os.path.join(mainDir, outputfile), outputdata, fmt='%26.18e')

    file.close()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    lb = "u"
    ax.plot(outputdata[1:-1, 0]/1000, outputdata[1:-1, 1]/1000, label=lb)
    lb = "v"
    ax.plot(outputdata[1:-1, 2]/1000, outputdata[1:-1, 3]/1000, label=lb)
    lb = "w"
    ax.plot(outputdata[1:-1, 4]/1000, outputdata[1:-1, 5]/1000, label=lb)
    ax.legend(numpoints=1)
    ax.grid(True)

    ax.ticklabel_format(axis='both', style='sci', scilimits=(-2, 2),useMathText=True)
    #fmt = matplotlib.ticker.StrMethodFormatter("{x:2.2e}")

    #ax.xaxis.set_major_formatter(fmt)
    #ax.yaxis.set_major_formatter(fmt)

    ax.set_xlabel('\\textbf{Applied field} (kA/m)')
    ax.set_ylabel('\\textbf{Magnetization} (kA/m)')
    #ax.set_title(r'\TeX\ is Number $\displaystyle\sum_{n=1}^\infty \frac{-e^{i\pi}}{2^n}$!', color='r')
    #fig.text(0.5, 1.01 ,r'\TeX\ is Number $\displaystyle\sum_{n=1}^\infty'
    #             r'\frac{-e^{i\pi}}{2^n}$!', color='r', horizontalalignment='center',transform = ax.transAxes)
    fig.text(0.5, 1.0, r'Hysteresis loop for permalloy squares of d=200 nm', color='r', horizontalalignment='center',transform = ax.transAxes)
    plt.tight_layout()
    #plt.subplots_adjust(top=0.995)
    plt.legend(loc='best')
    # plt.plot(Hexternal, mediau)

    plt.savefig(os.path.join(mainDir, outputplot), bbox_inches='tight', transparent=True,)
    plt.show()
    #
