#!/bin/bash
#SBATCH -n 36
#SBATCH --nodes=1
#SBATCH --gres=gpu:3
#SBATCH -t 02:00:00
#SBATCH -p gpu_v100


# run parameters
tpr="YOUR_TPR.tpr"
gmx_version=2019/skylake-gpu-basic
gmx_cmd="gmx mdrun -v -nsteps 15000 -resetstep 12000 -s $tpr  -noconfout -pin on -pinoffset 0 -nb gpu -pme gpu -npme 1"



source /shared/maylab/scripts/bash/modload.sh
modload gromacs/$gmx_version

# scan parameters for a full node gtx simulation

for nstlist in 80 100 120 140; do
    $gmx_cmd -nstlist $nstlist -g nstlist_${nstlist}_3rank  -ntmpi 3  -ntomp 12 -gputasks 012    
    $gmx_cmd -nstlist $nstlist -g nstlist_${nstlist}_6rank  -ntmpi 6  -ntomp  6 -gputasks 001122
    $gmx_cmd -nstlist $nstlist -g nstlist_${nstlist}_12rank -ntmpi 12 -ntomp  3 -gputasks 000011112222

    rm ./#*#
done
rm traj.trr ener.edr


printf "benchmarking performance in ns/day\nGromacs base command: $gmx_cmd\n" > performance.txt
grep Performance: *.log | sed "s/.log:Performance://"|  awk 'NF{NF-=1};1' | sort -k2 | column -t >> performance.txt
exit
