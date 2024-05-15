#!/bin/bash

cvmfs_server transaction ganga.cern.ch

cd /cvmfs/ganga.cern.ch/Ganga/install/DEV

micromamba activate

. bin/activate

pip uninstall --yes ganga

pip install --upgrade ganga[LHCb,Dirac]@git+https://github.com/ganga-devs/ganga.git@develop

# We need to uninstall htcondor from the default installation to use the preinstalled versions on cvmfs
pip uninstall --yes htcondor

deactivate

micromamba deactivate

cd ~

cvmfs_server publish ganga.cern.ch

