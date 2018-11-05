#!/bin/bash

# figures out the architecture based on the number of cpus
# prints out the architecture name, so you have to grab it
# with e.g. arch=`detect_architecture`
function detect_architecture {
  ncpus=`lscpu | grep '^CPU(s):' | awk '{print $2}'`
  
  case $ncpus in
    12) arch='westmere'    ;;
    16) arch='sandybridge' ;;
    20) model=`lscpu | grep '^Model:' | awk '{print $2}'`
	if [ $model -eq 62 ]; then
	  arch='ivybridge'
        elif [ $model -eq 79 ]; then
          arch='broadwell-gpu'
        else
	  arch="unknown - ncpus=$ncpus"
	fi ;;
    24) arch='haswell'     
        host=`hostname`
        if [ "${host:0:3}" = "gpu" ]; then
	    arch='haswell_gpu'
        fi;;
    36) arch='skylake'
        host=`hostname`
        if [ "${host:0:3}" = "gpu" ]; then
            arch='skylake_gpu'
        fi;;
    44) arch='broadwell'   ;;
    *)  arch="unknown - ncpus=$ncpus" ;;
  esac
  echo $arch
}
