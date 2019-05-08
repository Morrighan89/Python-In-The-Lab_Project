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



def sum_mag(time, file):
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


    data = np.append(data, [ summa[0,0], summa[0,1], summa[0,2]])
    return data


if __name__ == '__main__':
    #mainDir = "C:\\Projects\\Sally_adaptive_test_case"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\dot\\100\\t30"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Square\\200\\45\\parallel"
    #mainDir = "W:\\Micro\\Riccardo\\cfr2d3d_3d_random\\3d"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Sphere\\100"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\Cube\\50"
    #mainDir = "W:\\Micro\\Riccardo\\3D\\dot\\timeevolution\\preview"
    mainDir = "W:\\Micro\\Riccardo\\3D\\dot\\150"


    filename = "dot_156s28hy50b.h5"
    outputplot= filename.split(".", 1)[0] + ".pdf"
    outputplot = outputplot.split("_", 1)[0] + "_Hyst_" + outputplot.split("_", 1)[1]
    outputfile = filename.split(".", 1)[0] + ".dat"
    outputfile = outputfile.split("_", 1)[0] + "_sum_" + outputfile.split("_", 1)[1]

    print(outputfile)
    hdf5_file_name = os.path.join(mainDir, filename)

    dataset_numTimeSteps = '/TimestepsNumber'
    # dataset_Volumes ='/Volumes'
    event_number = 5

    versoreu = np.array([[0.6428],[0],[0.766]])
    versorev = np.array([[0], [1], [0]])
    versorew = np.array([[-0.766],[0],[0.6428]])
    # versoreT=np.reshape(versore,(1,3))
    file = h5py.File(hdf5_file_name, 'r')  # 'r' means that hdf5 file is open in read-only mode


    equilibria = [name.split('Emme',1)[1] for name in file if 'Emme' in name]
    equilibria = [int(i) for i in equilibria]

    datasetTime = file[dataset_numTimeSteps]
    # datasetVol=file[dataset_Volumes]
    numTimeSteps = datasetTime[(0)]
    print(numTimeSteps)

    outputdata = np.array([])
    # Volumes=np.array(datasetVol[()])

    for equilibrium in sorted(equilibria):
        outputdata = np.append(outputdata, sum_mag(equilibrium, file))

    print(np.shape(outputdata), "np.shape outputdata")
    outputdata = np.reshape(outputdata, (-1, 3))
    np.savetxt(os.path.join(mainDir, outputfile), outputdata, fmt='%26.18e')

    file.close()

