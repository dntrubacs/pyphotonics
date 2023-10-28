# pyphotonics  #
 
Python API used to control certain photonics experiments 
at the University of Southampton QLM group.

## Features ##
* Control of the BK Precision 4063B waveform generator via the `BKCom` communication class.
* Control of the Thorlabs KDC101 motors via `KDC101com`communication class.
* Control of the Sb2Se3 Optical Switching experiment via the `Sb2Sb3ExperimentControl` class.


## Getting Started ##
### Installation ###
Download Anaconda and create a conda environment with Python 3.11:
> conda create --name python=3.11

Activate the environment and install all the packages in the
`requiremnts.txt` file via pip. Open an IDE (such as PyCharm) and create
a project and choose the conda environment as interpreter. Open the cmd,
navigate to the directory and initialize a local repository (install git if 
it is not installed already):
>git init --initial-branch=main

Add this GitHub repo as remote origin:
> git remote add origin https://github.com/dntrubacs/pyphotonics.git

Pull the latest version of the code:
> git pull origin main

### How To Use ###
For now, only the Sb2Se3 Optical Switching experiment can be controlled. To 
do this, import the `Sb2Sb3ExperimentControl` class from the 
`experiments.sb2_sb3_optical_switching` module. Firstly use the `calibrate` method to
setup the experiment (home the motors and check whether the waveform generator
is working). After that, use the `run_experiment` to start writing pixels on the material.


## Updates ## 
Last updated by Daniel-Iosif Trubacs on 28 October 2023.