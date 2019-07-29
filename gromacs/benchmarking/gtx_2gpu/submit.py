import shutil
import os

tpr = "part1.tpr"
slurm = "sub.sh"

njobs = [1, 2, 4, 10]
steps = 15000


for nj in njobs:
	destdir = "nj"+str(nj)
	if os.path.exists(destdir) == False:
		os.mkdir(destdir)
	command = "cp " +slurm + " "+destdir+"/sub.sh"
	os.system(command)
	command = "cp " +tpr + " "+destdir+"/."
	os.system(command)
	os.chdir(destdir)
	f=open("sub.sh", "a")
	f.write("tpr=" + tpr+"\n")
	if nj == 1:
		gmx_command="gmx mdrun -s $tpr -nsteps " +str(steps) +" -ntmpi 4 -ntomp 5 -gputasks 0001 -pin on -pinoffset 0 -nb gpu -pme gpu -npme 1\n"
		f.write(gmx_command)
		f.write("exit")
		f.close()
		command = "sbatch sub.sh"
		os.system(command)
	elif nj == 2:
		gmx_command1 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job1 -ntmpi 2 -ntomp 5 -gputasks 00 -pin on -pinoffset 0 -nb gpu -pme gpu -npme 1 &\n"
		gmx_command2 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job2 -ntmpi 2 -ntomp 5 -gputasks 11 -pin on -pinoffset 10 -nb gpu -pme gpu -npme 1 \n"
		f.write(gmx_command1)
		f.write(gmx_command2)
		f.write("wait \n exit")
		f.close()
		command = "sbatch sub.sh"
		os.system(command)
	elif nj == 4:
		gmx_command1 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job1 -ntmpi 1 -ntomp 5 -gputasks 00 -pin on -pinoffset 0 -nb gpu -pme gpu  &\n"
		gmx_command2 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job2 -ntmpi 1 -ntomp 5 -gputasks 00 -pin on -pinoffset 5 -nb gpu -pme gpu  &\n"
		gmx_command3 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job3 -ntmpi 1 -ntomp 5 -gputasks 11 -pin on -pinoffset 10 -nb gpu -pme gpu &\n"
		gmx_command4 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job4 -ntmpi 1 -ntomp 5 -gputasks 11 -pin on -pinoffset 15 -nb gpu -pme gpu \n"
		f.write(gmx_command1)
		f.write(gmx_command2)
		f.write(gmx_command3)
		f.write(gmx_command4)
		f.write("wait \n exit")
		f.close()
		command = "sbatch sub.sh"
		os.system(command)
	elif nj == 10:
		gmx_command1 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job1 -ntmpi 1 -ntomp 2 -gputasks 00 -pin on -pinoffset 0 -nb gpu -pme gpu  &\n"
		gmx_command2 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job2 -ntmpi 1 -ntomp 2 -gputasks 00 -pin on -pinoffset 2 -nb gpu -pme gpu  &\n"
		gmx_command3 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job3 -ntmpi 1 -ntomp 2 -gputasks 00 -pin on -pinoffset 4 -nb gpu -pme gpu  &\n"
		gmx_command4 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job4 -ntmpi 1 -ntomp 2 -gputasks 00 -pin on -pinoffset 6 -nb gpu -pme gpu  &\n"
		gmx_command5 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job5 -ntmpi 1 -ntomp 2 -gputasks 00 -pin on -pinoffset 8 -nb gpu -pme gpu  &\n"
		gmx_command6 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job6 -ntmpi 1 -ntomp 2 -gputasks 11 -pin on -pinoffset 10 -nb gpu -pme gpu  &\n"
		gmx_command7 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job7 -ntmpi 1 -ntomp 2 -gputasks 11 -pin on -pinoffset 12 -nb gpu -pme gpu  &\n"
		gmx_command8 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job8 -ntmpi 1 -ntomp 2 -gputasks 11 -pin on -pinoffset 14 -nb gpu -pme gpu  &\n"
		gmx_command9 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job9 -ntmpi 1 -ntomp 2 -gputasks 11 -pin on -pinoffset 16 -nb gpu -pme gpu  &\n"
		gmx_command10 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -deffnm job10 -ntmpi 1 -ntomp 2 -gputasks 11 -pin on -pinoffset 18 -nb gpu -pme gpu  \n"
		f.write(gmx_command1)
		f.write(gmx_command2)
		f.write(gmx_command3)
		f.write(gmx_command4)
		f.write(gmx_command5)
		f.write(gmx_command6)
		f.write(gmx_command7)
		f.write(gmx_command8)
		f.write(gmx_command9)
		f.write(gmx_command10)
		f.write("wait \n exit")
		f.close()
		command = "sbatch sub.sh"
		os.system(command)
	os.chdir("..")
