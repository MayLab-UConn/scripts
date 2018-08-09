#!/bin/bash

# figures out the architecture based on the number of cpus
# prints out the architecture name, so you have to grab it
# with e.g. arch=`detect_architecture`
function detect_architecture {
  ncpus=`lscpu | grep '^CPU(s):' | awk '{print $2}'`
  
  case $ncpus in
    12) arch='westmere'    ;;
    16) arch='sandybridge' ;;
    20) arch='ivybridge'   ;; # NOTE - THIS WILL CONFLICT WITH BROADWELL IN FUTURE
    24) arch='haswell'     ;;
    44) arch='broadwell'   ;;
    *)  arch="unknown - ncpus=$ncpus" ;;
  esac
  echo $arch
}
