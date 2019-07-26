#!/bin/bash
#SBATCH --nodes=1
#SBATCH -n 20
#SBATCH -p GtxPriority
#SBATCH --exclude=gtx[01]  
#SBATCH --gres=gpu:2
#SBATCH -t 12:00:00


source /shared/maylab/scripts/bash/modload.sh
modload gromacs/2019/broadwell-gpu-basic




