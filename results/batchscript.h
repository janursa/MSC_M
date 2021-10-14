#!/bin/bash
#SBATCH --partition=all
#SBATCH --time=01:00:00                           # Maximum time requested
#SBATCH --nodes=1                                 # Number of nodes
#SBATCH --chdir   ./      # directory must already exist!
#SBATCH --job-name  calib
#SBATCH --output    calib-%N-%j.out            # File to which STDOUT will be written
#SBATCH --error     calib-%N-%j.err            # File to which STDERR will be written
#SBATCH --mail-type ALL                           # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user jalil.nourisa@hzg.de            # Email to which notifications will be sent. It defaults to 
unset LD_PRELOAD
source /etc/profile.d/modules.sh
module load maxwell gcc/8.2
module load mpi/openmpi-x86_64
export PYTHONPATH=/usr/lib64/python3.6/site-packages/openmpi
mpiexec -np 20 --mca pml ob1 python3 ../calibration/batch_calibration.py
