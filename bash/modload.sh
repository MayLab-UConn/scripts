#!/bin/bash


# formatting function - with offset variable in modload, formats reporting so that the recursive loading
# of modules is clear
function tabprint {
    str_in="$1"
    tabs=$2
    for i in `seq $tabs`; do printf "   "; done
    printf "%s\n" "$str_in"
}



# given a module purge prefix (such as would be in the "conflict" field of a mod file, look through loaded
# module and purge anything starting with that prefix
function modpurge {
  module_to_purge=$1
  modlist=$((module list) 2>&1)    # module list goes to stderr, 2>&1 is to capture it like it was stdout
  for modword in $modlist; do
    if [[ $modword == "${module_to_purge}"* ]]; then
        tabprint "Unloading $modword" $offset
        module unload $modword
    fi
  done
}


# Loads a given module and its dependencies, unloads conflicts
function modload {
  
  # this is for formatting - is incremented and decremented with recursive calls
  if [ -z "$offset" ]; then
    offset=0
  fi

  # these variables are local because they're reinstantiated in recursive calls
  local module_to_load=$1
  tabprint "Attempting to load  $module_to_load" $offset
  local mod_info=$((module show $module_to_load) 2>&1)  # redirect from stderr

  offset=$((offset + 1))
  # remove conflicting loaded modules using modpurge
  for conflict in `echo "$mod_info" | grep "^conflict" | awk '{print $2}'`; do
    tabprint "Checking for conflicts of $module_to_load - $conflict" $offset
    modpurge $conflict
  done

  # load prereqs recursively using modload
  for prereq in ` echo "$mod_info" | grep "^prereq" | awk '{print $2}'`; do
    modload $prereq
  done

  offset=$((offset - 1))
  # finally load the module
  module load $module_to_load
  if [ $? -eq 0 ]; then
    tabprint "Loaded $module_to_load" $offset
  fi
}

