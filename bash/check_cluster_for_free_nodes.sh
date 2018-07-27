#!/bin/bash

# Checks hornet cluster for idle nodes, categorizes by partition and architecture
# author: Kevin Boyd

# -----------------------------------------------------------------------------------------------------
# constants about the cluster
# -----------------------------------------------------------------------------------------------------
n_gpu_nodes=2
n_maylab_nodes=11

declare -A node_archs
node_archs=(["broadwell"]="cn[325-328]" 
            ["haswell"]="cn[137-324"] 
            ["ivy_bridge"]="cn[105-136]" 
            ["sandy_bridge"]="cn[65-104]" )

normal_partitions="general general_requeue parallel serial"
architectures="broadwell haswell ivy_bridge sandy_bridge"

# -----------------------------------------------------------------------------------------------------                                                                                                        
# functions                                                                                                                                                                                  
# -----------------------------------------------------------------------------------------------------   

function get_sq_nodes () {
    # parameters are qos, and running status (R/PD)                                                                                                                                                                # prints a total number of nodes -  capture output with command substitution                                                                                                                               
    echo `squeue -a -h --format=%2D -q $1 -t $2 |  awk '{s+=$1}END{print s}'`
}   

function get_sinfo_nodes () {
    echo `sinfo -h -p $1 -t $2 --format=%2D`
}

# -----------------------------------------------------------------------------------------------------                                                                                                        
# special partitions                                                                                                                                                                                  
# -----------------------------------------------------------------------------------------------------   

# first maylab, -q for qos, -t to select running ("R") or pending "PD", %D for number of nodes, then the paste and bc commands to sum up columns
# -h option removes header
n_may_running=$( get_sq_nodes maylab R ) 
n_may_pending=$( get_sq_nodes maylab PD )
n_may_available=$((n_maylab_nodes - n_may_running))


# next, check gpu
n_gpu_running=$( get_sinfo_nodes gpu alloc )
n_gpu_avail=$(( n_gpu_nodes - n_gpu_running ))
n_gpu_pending=`squeue -a -h --format=%2D -p gpu -t PD | awk '{s+=$1} END {print s}'`


# -----------------------------------------------------------------------------------------------------                                                                                                        
# normal partitions                                                                                                                                                                                  
# -----------------------------------------------------------------------------------------------------   

printf "\n%-15s %14s %18s\n--------------------------------------------------\n" "partition" "architecture" "nodes available"
printf "%-15s %14s %18d\n" "maylab" "ivy_bridge" $n_may_available
printf "%-15s %14s %18d\n\n" "gpu" "haswell-gpu" $n_gpu_avail 


# check parallel
for part in $normal_partitions; do
    for arch in $architectures; do
	n_avail=`sinfo -h --format=%2D -p $part --nodes=${node_archs[$arch]} -t idle |  awk '{s+=$1}END{print s}'`
	if [ ! -z "$n_avail" ] ; then
	    printf "%-15s %14s %18d\n" $part $arch $n_avail
	fi
    done
done

printf "\n"

exit
