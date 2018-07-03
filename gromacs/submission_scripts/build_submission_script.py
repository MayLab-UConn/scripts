#!/usr/bin/python3

partitions = ['general', 'general_requeue', 'serial', 'maylab', 'parallel', 'gpu']
gmx_versions = ['gmx5', 'gmx2016', 'gmx2018']

partition_times = {
    'general'         : '12:00:00',
    'general_requeue' : '12:00:00',
    'serial'          : '48:00:00',  # personal limit, actual is 7 days
    'maylab'          : '36:00:00',
    'parallel'        : '06:00:00',
    'gpu'             : '12:00:00'
}

partition_architectures = {
    'general'         : ['haswell', 'sandy_bridge', 'ivy_bridge'],
    'general_requeue' : ['haswell'],
    'serial'          : ['haswell'],
    'maylab'          : ['ivy_bridge'],
    'parallel'        : ['haswell'],
    'gpu'             : ['haswell']
}

partition_node_maxes = {
    'general'         : 8,
    'general_requeue' : 8,
    'serial'          : 1,
    'maylab'          : 11,
    'parallel'        : 16,
    'gpu'             : 1
}

arch_cores_per_node = {
    'sandy_bridge' : 16,
    'ivy_bridge'   : 20,
    'haswell'      : 24,
    'haswell_gpu'  : 24,
    'broadwell'    : 44
}

arch_exclusions = {
    'sandy_bridge' : "cn[01-64,105-320,325-328]",
    'ivy_bridge'   : "cn[01-104,137-320,325-328]",
    'haswell'      : "cn[01-136,325-328]",
    'haswell_gpu'  : "cn[01-136,325-328]",
    'broadwell'    : "cn[01-320]"
}

mpi_gmx_commands = {
    'sandy_bridge' :  {
        'gmx5' : "srun gmx_mpi"
    },
    'ivy_bridge'   :  {
        'gmx5'    : "srun gmx_mpi",
        'gmx2016' : "srun --mpi=pmi2 gmx_mpi",
        'gmx2018' : "srun --mpi=pmi2 gmx_mpi"
    },
    'haswell'      :  {
        'gmx5'    : "srun gmx_mpi",
        'gmx2016' : "srun --mpi=pmi2 gmx_mpi",
        'gmx2018' : "srun --mpi=pmi2 gmx_mpi"
    }

}


mpi_modules = {
    'sandy_bridge' :  {
        'gmx5' : ('module load ...',)
    },

    'ivy_bridge'   :  {
        'gmx5'    : "module load intelics/2013.1.039-full gromacs/5.0.1-ics\n" +
                    "export I_MPI_PMI_LIBRARY=/gpfs/gpfs1/slurm/lib/libpmi.so\n" +
                    "export I_MPI_FABRICS=shm:ofa",
        'gmx2016' : "module load gcc/5.4.0 mpi/openmpi/1.10.3 hwloc/1.11.3 gromacs/2016-mpi-ivybridge",
        'gmx2018' : "module load gcc/7.3.0 hwloc/1.5.2  mpi/openmpi/3.0.0  gromacs/2018-ivybridge-mpi"
    },
    'haswell'      :  {
        'gmx5'    : "module load intelics/2013.1.039-full gromacs/5.0.1-ics-haswell\n" +
                    "export I_MPI_PMI_LIBRARY=/gpfs/gpfs1/slurm/lib/libpmi.so\n" +
                    "export I_MPI_FABRICS=shm:ofa",
        'gmx2016' : "module load hwloc/1.11.3  mpi/openmpi/1.10.3 gcc/5.4.0 gromacs/2016-mpi-haswell",
        'gmx2018' : "module load gcc/7.3.0 hwloc/1.5.2  mpi/openmpi/3.0.0  gromacs/2018-haswell-mpi"
    },
    'haswell-gpu'  :  {

    },
    'broadwell'    :  {

    }
}

non_mpi_modules = {
    'sandy_bridge' :  {
        'gmx5' : ('module load ...',)
    },
    'ivy_bridge'   :  {

    },
    'haswell'      :  {

    },
    'haswell-gpu'  :  {
        'gmx5'    : "",
        'gmx2016' : "module load gcc/5.4.0-alt hwloc/1.11.3 cuda/8.0 gromacs/2016.4-gpu",
        'gmx2018' : "module load gcc/7.3.0 hwloc/1.5.2 cuda/8.0 gromacs/2018-haswell-gpu"
    },
    'broadwell'    :  {

    }

}


# --------------------------------------------------------------------------------------------------------------------
# interactive selection
# -------------------------------------------------------------------------------------------------------------------

def user_input_from_options(variable, options):

    def get_selected_input(variable, options):
        return input("Choose " + variable + '. Options are:\n' + '\n'.join(options) + '\n\n')

    return_value = ''
    while return_value not in options:
        return_value = get_selected_input(variable, options)
        if return_value not in options:
            print("Invalid " + variable + " chosen, try again\n")
    print("You have chosen " + variable + " = " + return_value)
    return return_value


def user_input_integer(msg, minint, maxint):
    return_ready = False
    while not return_ready:
        return_string = input(msg)
        if not return_string.isdigit():
            print("Did not enter an integer, try again")
        else:
            return_int = int(return_string)
            if return_int < minint:
                print("Invalid number, must be greater or equal to " + str(minint))
            elif return_int > maxint:
                print("Invalid number, must be less than or equal to " + str(maxint))
            else:
                return_ready = True
    return return_int


# partition
partition = user_input_from_options('partition', partitions)

# architecture
if len(partition_architectures[partition]) == 1:   # if no choice, ie ivy bridge for maylab
    architecture = partition_architectures[partition][0]
    print("For partition = {}, the only architecture possible is {}\n".format(partition, architecture))
else:
    architecture = user_input_from_options('architecture', partition_architectures[partition])

# nodes
if partition_node_maxes[partition] > 1:
    nodes = user_input_integer("\nSelect number of nodes. Note that the maximum value for partition = {} is {}\n".format(  # noqa
                               partition, partition_node_maxes[partition]),
                               1, partition_node_maxes[partition])
else:
    print("With partition = {}, only one node can be used")
    nodes = 1

# gromacs version
gmx_version = user_input_from_options("Gromacs version", gmx_versions)

# mpi or not
if nodes > 1:
    use_mpi = True
else:
    if gmx_version in mpi_modules[architecture] and gmx_version in non_mpi_modules[architecture]:
        print("With this combination of architecture and gromacs version, and on 1 node, you can choose an " +
              "mpi-enabled or non-mpi-enabled gromacs installation. All other things equal, you typically don't " +
              "want to use the mpi version if you don't have to - it comes with some performance overhead, but your "
              "specific case might require it for whatever reason.\n")
        chosen_mpi = user_input_from_options('mpi ', ('enabled', 'disabled'))
        use_mpi = chosen_mpi == 'enabled'

if use_mpi:
    module_matrix = mpi_modules
else:
    module_matrix = non_mpi_modules

in_script = input("Do you have a template script? Enter the path here, and the output script will contain the same " +
                  "commands as the template script, modified for mpi if that option has been chosen. If not (and " +
                  "you just want the header and module command written, hit enter\n")

out_script = input("Name your output script. Defaults to slurm_run.sh\n")
if not out_script:
    out_script = "slurm_run.sh"

with open(out_script, 'wt') as fout:
    fout.write("#!/bin/bash\n")
    fout.write("#SBATCH -p {}\n".format(partition))
    fout.write("#SBATCH -t {}\n".format(partition_times[partition]))
    fout.write("#SBATCH -N {}\n".format(nodes))
    fout.write("#SBATCH -n {:d}\n".format(nodes * arch_cores_per_node[architecture]))
    fout.write("#SBATCH --exclude={}\n".format(arch_exclusions[architecture]))

    if partition == "gpu":
        fout.write("#SBATCH --gres=gpu:2\n")

    fout.write("\n\n{}\n".format(module_matrix[architecture][gmx_version]))

    if use_mpi:
        command_prefix = mpi_gmx_commands[architecture][gmx_version]
    else:
        command_prefix = 'gmx'

    if in_script:
        try:
            with open(in_script, 'r') as fin:
                for line in fin:
                    fout.write(line.replace("gmx", command_prefix))
        except FileNotFoundError:
            print("Template script {} not found, will write an example mdrun command".format(in_script))
            fout.write("{} mdrun -deffnm tprprefix\n".format(command_prefix))
    else:
        fout.write("{} mdrun -deffnm tprprefix\n".format(command_prefix))

    fout.write('\nexit\n')
