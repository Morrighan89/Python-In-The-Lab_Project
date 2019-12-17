# **SallyLLG Data analysis** - Python Functions for **SallyLLG** simulation analysis

**SallyLLG Data analysis** provides a series of different function to comèpute the hysteresi cycle from the data obtained with the micromagnetic code SallyLLG in the *.h5* format. It can be used both with the results provided by the 2D 2.5D and 3D code.

## Get started

Copy the  .py files from this repository in the working folder


## Documentation

Three main scripts can be found:
  `hdf5_test.py`, which contains the routines to compute the hysteresis cycle of from the 2.5d and 2d simulations;
  `hdf5_test_3Dv2.py`, which contains the routines to compute the hysteresis cycle of from the 3d simulations;
  `distributions4_corrections.py`, which allows to plot the data obtained from the previous scripts;

### List of hdf5_test.py functions

"""
Basic script Open a HDF5 file of my simulation and compute the Hysteresis loop, saves data in an opportune file with specific naming pattern
at the end plots the calculated loop.
"""

```python
calcoloMagnMedia(time,file,Volumes)
```
Return a the average magnetization for each time step / equilibrium point of the simultaion.

```python
calcoloMagnMediaDisks(time,file,Volumes,numDisks)
```
Return a the average magnetization for each time step / equilibrium point of the simultaion, for each object in a 2.5D distribution of N objects.

```python
calcoloEnergia(time,file,Volumes):
```
Computes the Zeeman and magnetostatric energy of the system for each time step / equilibrium point.


### List of hdf5_test_3Dv2.py functions

"""
Basic script Open a HDF5 file of my simulation and compute the Hysteresis loop, saves data in an opportune file with specific naming pattern
at the end plots the calculated loop.
"""

```python
MagnetizationCalc(mainDir,filename):
```
Sets up the class and loads the *filename.h5* file from the folder in *mainDir*.

```python
computeData(self, hysteresis=True, dt=1, versoreu = np.array([[1],[0],[0]]), versorev = np.array([[0],[1],[0]]), versorew = np.array([[0],[0],[1]])):
```
Evaluate the Hysteresis loop or the average magnetization temporal behaviour along the direction specified by the versors *versoreu, versorev, verosew*.

```python
calcoloMagnMediaVsappField(time, file, versoreu, versorev, versorew):
```
Used in `computeData` to evaluate the Hysteresis loop.

```python
calcoloMagnMedia(time, file, versoreu, versorev, versorew):
```
Used in `computeData` to evaluate the temporal behaviour of the magnetization