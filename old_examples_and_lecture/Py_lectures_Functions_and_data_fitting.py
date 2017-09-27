
# coding: utf-8

# # Python-in-the-lab: function and data fitting

# In[42]:

import os
import numpy as np
import scipy.integrate as integrate
import matplotlib.pylab as plt
from scipy.optimize import curve_fit

parameters3p = ["gamma", "A1", "A2"]
def fitShape3p(x, gamma, a1, a2):
    """
    fitting function for the average shape
    
    Parameters:
    ===========
    a1: float
        amplitude
    a2: float
        constant of the exponential
    gamma: float
        exponent of the shape
    """
    return a1*(x*(1-x))**(gamma-1) * np.exp(-a2*x)

parameters2p = parameters3p[:-1]
def fitShape2p(x, gamma, a):
    """
    fitting function for the average shape
    
    Parameters:
    ===========
    a: float
        constant of the exponential
    gamma: float
        exponent of the shape
    """
    f = (x*(1-x))**(gamma-1) * np.exp(-a * x)
    norm = integrate.trapz(f, x)
    return f/norm


# In[43]:

mainDir = "/home/gf/src/Python/Python-in-the-lab/Bk"
# Today we use the same file of the shapes
filename = "F64ac_0.02_time_V_T.dat"
filename = os.path.join(mainDir, filename)
data = np.loadtxt(filename, comments="#")
time = data[:,0]
with open(filename) as f:
    header = f.readline()
sizes = [float(size) for size in header.split()[1:]]
shapes = dict()
for i, size in enumerate(sizes):
    shapes[size] = data[:,i+1]


# ## Next Problems
# ## 1. Make the average of the 8 normalized curves (You can do it)

# ### Try to solve the problem above by yourself. Anyway, a possible solution is found below

# Get the average of the 8 curves
#average = np.zeros_like(shapes[size]) # Ahah, this is not required!
average = 0
for size in shapes:
    shape = shapes[size]
    average += shape/integrate.trapz(shape,time)
average /= len(shapes)

for size in sorted(shapes):
    lb = "{0:.2e}".format(size)
    shape = shapes[size]
    norm = integrate.trapz(shapes[size], time)
    plt.plot(time, shapes[size]/norm, label=lb)
plt.legend(ncol=2,loc=(0.15,.05))
plt.plot(time, average, 'k', lw=3);


# ## 2. Make a fit of the average curve with 
# ## $[x(1-x)]^\gamma * exp(-Ax)$, 
# 

popt, pcov = curve_fit(fitShape3p, time, average)
for p, diag, parameter in zip(popt,pcov.diagonal(),parameters):
    print("Parameter {0} = {1:.3f} +/- {2:.3f}".format(parameter, p, diag**0.5))
# pcov.diagonal()**0.5 # These are the errors of the fitting parameters at 1 sigma


# ## Hold on! I guess there are too many parameters... 
# 
# ### Yes, the average should have an integral equal to 1, or not?
# 
# #### Let's check it

print("Normalization of the average is %f" % integrate.trapz(average, time))


popt, pcov = curve_fit(fitShape2, time, average)
for p, diag, parameter in zip(popt,pcov.diagonal(),parameters):
    print("Parameter {0} = {1:.3f} +/- {2:.3f}".format(parameter, p, diag**0.5))
#pcov.diagonal()**0.5 # These are the errors of the fitting parameters at 1 sigma


# In[49]:

plt.plot(time, average, 'bo')
plt.plot(time, fitShape(time, *popt), '-r', lw=2) # Note the use of *popt
plt.plot(time, fitShape(time, popt[0], 0), '--r', lw=1) # What did I do?
plt.xlabel("time", size=16)
plt.ylabel("average shape (normalized)", size=14)


# # Fitting is so important in the lab... let's explore it a little bit


# # Ok, man, this is a serious problem
# 
# I am doing an average over 8 curves, I think I can estimate an error bar for each point, can I?
# 
# But then should I use it for doing what? Weight or error?
# 
# and...
# 
# ### Does the fitting parameters and their errors depend on this choice???

# ### Problem: calculate the error bars, and use them in the fitting fuction. Show if the fitting parameters change and their error

# In[88]:

# The solution goes here...
variances = np.array([np.var(row) for row in data[:,1:]])
err_average = (variances/len(row))**0.5
popt1, pcov1 = curve_fit(fitShape, time, average, p0=(1.6,0.5), sigma=err_average)
for p, diag, parameter in zip(popt1,pcov1.diagonal(),parameters):
    print("Parameter {0} = {1:.4f} +/- {2:.4f}".format(parameter, p, diag**0.5))
plt.plot(time, average, 'bo')
plt.plot(time, fitShape(time, *popt), '-b', lw=2) # Note the use of *popt
popt2, pcov2 = curve_fit(fitShape, time, average, p0=(1.6,0.5), sigma=err_average, absolute_sigma=True)
for p, diag, parameter in zip(popt2,pcov2.diagonal(),parameters):
    print("Parameter {0} = {1:.4f} +/- {2:.4f}".format(parameter, p, diag**0.5))


# In[56]:

# Explore the function
print(fitShape.__doc__)


# In[57]:

# Can we make a running code out of the notebook? Let's do it!


# In[59]:

fitShape.__name__


# In[ ]:



