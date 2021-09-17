#!/bin/bash
#SBATCH --partition=all
#SBATCH --time=00:30:00                           # Maximum time requested
#SBATCH --nodes=1                                 # Number of nodes
#SBATCH --chdir   ./      # directory must already exist!
#SBATCH --job-name  SA
#SBATCH --output    SA-%N-%j.out            # File to which STDOUT will be written
#SBATCH --error     SA-%N-%j.err            # File to which STDERR will be written
#SBATCH --mail-type ALL                           # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user jalil.nourisa@hzg.de            # Email to which notifications will be sent. It defaults to 
unset LD_PRELOAD
source /etc/profile.d/modules.sh

python3 diff_calibration.py
