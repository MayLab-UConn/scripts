#!/bin/bash --login
#SBATCH --partition=gpu_v100
#SBATCH -t 00:30:00
#SBATCH -c 12

# Example install script for new gromacs versions. This should be run from the top
# directory of the gromacs source folder. The program will be installed in
# $app_path/$program_name/$install_type, which for maylab use ends up being
# /shared/maylab/mayapps/gromacs/versionumber/architecture_details
#
# After installing, a module file needs to be made, which for a specific gromacs version
# should be put in $app_path/mod/$program_name/$install_type, and the requisite description
# and requirements modified 
#
# Remember to change the sbatch lines to target the architecture you want the program installed on

# paths and naming. In this example, we're installing vanilla Gromacs 2019, to run on the
# skylake nodes with v100s
app_path=/shared/maylab/mayapps
program_name=gromacs/2019
install_type=skylake-gpu

# cmake options for how we want gromacs compiled. 
AVX=AVX2_256  # apparently faster than 512 with GPU runs, but on non-gpu skylake, use AVX_512
GPU=ON        # Off for CPU-only MPI runs - if on, make sure cuda is loaded
MPI=OFF       # On for CPU-only MPI runs  - if on, make sure openmpi is loaded (mpi/openmpi/3.0.0)

# set the path for our custom installs of the hwloc library and fftw, because cmake
# tends to accidentally find the default hornet versions even when we've loaded the module
PREFIXPATH="$app_path/hwloc/1.11.10;$app_path/fftw/3.3.8;"


# module stuff, don't mess with this
export MODULEPATH=$app_path/mod:$MODULEPATH    # make sure we have access to maylab modules
unset INCLUDE LD_LIBRARY_PATH                  # some issues with cmake app selection, idk if we really need this anymore
module purge                                   # start from a module-free state

# maylab modules
module load gcc/6.4.0 \
            cmake/3.4.3 \
            hwloc/1.11.10 \
            fftw/3.3.8 
# cluster modules
module load binutils/2.26 \
            zlib/1.2.8 \
            python/2.7.6 \
            cuda/9.1
# ---------------------------------------------------------------------------------                                                          
# should not have to modify anything below this point                                                                                        
# --------------------------------------------------------------------------------- 

# compiler flags and accounting for cmake struggling to find the right c compilers
export CPPFLAGS=$(echo "-I${INCLUDE//:/ -I}")      # no clue about these two but afraid to remove
export LDFLAGS=$(echo "-L${LD_LIBRARY_PATH//:/ -L}")
export CC=`which gcc`   # loaded by now so will point to loaded module
export CXX=`which g++`  # same


# create and enter build directory
if [ -d $install_type ]; then
    rm -r $install_type
fi
mkdir $install_type
cd $install_type


# do the install
cmake -DCMAKE_INSTALL_PREFIX="$app_path/$program_name/$install_type" \
      -DCMAKE_PREFIX_PATH=$PREFIXPATH \
      -DGMX_MPI=$MPI \
      -DGMX_GPU=$GPU \
      -DGMX_SIMD=$AVX ..
make --jobs=$SLURM_CPUS_PER_TASK &&
make --jobs=$SLURM_CPUS_PER_TASK install
