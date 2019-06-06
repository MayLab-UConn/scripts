#!/bin/bash
#SBATCH -n 20
#SBATCH -N 1
#SBATCH --gres=gpu:2
#SBATCH -p GtxPriority
#SBATCH -t 96:00:00
#SBATCH --exclude=gtx01

# This is a sample script to demonstrate how one can run 4 jobs at a time
# on a single GPU node, in this case a Gtx node with 2 GPUs (because gtx01 is excluded).
#
# The setup here is that I have a number of umbrella windows to run on a distance-based
# reaction coordinate. This script should be submitted from a directory where each subdirectory
# contains a tpr for a specific window.
#
# For this specific example, the folders are named 10.0nm, 10.5nm, and so on
# My tpr in each folder is step7_production.tpr
# On a 20 core gtx node with 2 gpus, the jobs will run in parallel as follows
# job1 - cores 0-4,   card 0
# job2 - cores 5-9,   card 0
# job3 - cores 10-14, card 1
# job4 - cores 15-19, card 1

# use maylab modload
source /shared/maylab/scripts/bash/modload.sh
modload gromacs/2019/broadwell-gpu-basic

# job parameters
njobs=4                              # how many jobs to run on this node
dirs=(10.0nm 10.5nm 11.0nm 11.5nm)   # the directories we'll be running in
pinoffsets=(0 5 10 15)               # this combined with ntomp defines the cores for each job
gpus=(0 0 1 1)                       # the GPU id for each job

# simulation parameters                                                                                                                                                                                           
simname=step7_production 
ntomp=5
maxh=95.8
nstlist=80
common="gmx mdrun -deffnm $simname -cpi $simname -pf ${simname}_pullf.xvg -px ${simname}_pullx.xvg -nb gpu -pin on -ntmpi 1 -ntomp $ntomp -maxh $maxh -nstlist $nstlist"




# ------------------------------------------------------
# should not need to change below here
# -----------------------------------------------------
topdir=`pwd`

# arrays are zero indexed                                                                                                                                                                                          
for i in `seq 0 $((njobs - 2))`; do
    cd "$topdir/${dirs[i]}"
    $common -gputasks ${gpus[i]} -pinoffset ${pinoffsets[i]} &
done

# do last job without subprocess ampersand                                                                            
i=$((njobs - 1))
cd "$topdir/${dirs[i]}"
$common -gputasks ${gpus[i]} -pinoffset ${pinoffsets[i]}




exit
