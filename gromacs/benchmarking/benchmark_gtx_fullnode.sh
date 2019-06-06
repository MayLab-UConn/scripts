#!/bin/bash
#SBATCH -n 20
#SBATCH --nodes=1
#SBATCH --gres=gpu:2
#SBATCH -t 02:00:00
#SBATCH -p GtxPriority


# run parameters
tpr="YOUR_TPR.tpr"
gmx_cmd="gmx mdrun -v -nsteps 15000 -resetstep 12000 -s $tpr  -noconfout -pin on -pinoffset 0 -nb gpu -pme gpu -npme 1"



source /shared/maylab/scripts/bash/modload.sh
modload gromacs/2018.3/broadwell-gpu-basic

# scan parameters for a full node gtx simulation

for nstlist in 80 100 120 140; do
    $gmx_cmd -nstlist $nstlist -g nstlist_${nstlist}_2rank  -ntmpi 2  -ntomp 10 -gputasks 01
    $gmx_cmd -nstlist $nstlist -g nstlist_${nstlist}_4rank  -ntmpi 4  -ntomp  5 -gputasks 0011
    $gmx_cmd -nstlist $nstlist -g nstlist_${nstlist}_10rank -ntmpi 10 -ntomp  2 -gputasks 0000011111

    rm ./#*#
done
rm traj.trr ener.edr


printf "benchmarking performance in ns/day\nGromacs base command: $gmx_cmd\n" > performance.txt
grep Performance: *.log | sed "s/.log:Performance://"|  awk 'NF{NF-=1};1' | sort -k2 | column -t >> performance.txt
exit
