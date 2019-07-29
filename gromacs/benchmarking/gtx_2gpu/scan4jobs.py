import shutil
import os

tpr = "part1.tpr"
slurm = "sub.sh"

steps = 15000
ntmpi = 1
ntomp = [2, 4, 5, 10]
nstlist = [40, 80, 160, 320]
for nl in nstlist:
	for nt in ntomp:
		destdir = "nj4/ntomp"+str(nt)+"/nst"+str(nl)
		if os.path.exists(destdir) == False:
			os.mkdir(destdir)
		command = "cp " +slurm + " "+destdir+"/sub.sh"
		os.system(command)
		command = "cp " +tpr + " "+destdir+"/."
		os.system(command)
		os.chdir(destdir)
		f=open("sub.sh", "a")
		f.write("tpr=" + tpr+"\n")
		gmx_command1 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -nstlist "+str(nl)+ " -deffnm job1 -ntmpi " + str(ntmpi) +" -ntomp "+str(nt) +" -gputasks 00 -pin on -pinoffset 0 -nb gpu -pme gpu &\n"
		gmx_command2 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -nstlist "+str(nl)+ " -deffnm job2 -ntmpi "  + str(ntmpi) +" -ntomp "+str(nt) +" -gputasks 00 -pin on -pinoffset 5 -nb gpu -pme gpu &\n"
		gmx_command3 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -nstlist "+str(nl)+ " -deffnm job3 -ntmpi " + str(ntmpi) +" -ntomp "+str(nt) +" -gputasks 11 -pin on -pinoffset 10 -nb gpu -pme gpu  &\n"
		gmx_command4 = "gmx mdrun -s $tpr -nsteps " +str(steps) +" -nstlist "+str(nl)+ " -deffnm job4 -ntmpi " + str(ntmpi) +" -ntomp "+str(nt) +" -gputasks 11 -pin on -pinoffset 15 -nb gpu -pme gpu \n"
		f.write(gmx_command1)
		f.write(gmx_command2)
		f.write(gmx_command3)
		f.write(gmx_command4)
		f.write("wait \n exit")
		f.close()
		command = "sbatch sub.sh"
		os.system(command)
		os.chdir("../../..")

