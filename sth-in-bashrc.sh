#!/bin/bash

# get .pdb file in RCSB with PDB ID
# use: getpdb 2HAC
function getpdb() {
    wget files.rcsb.org/download/$1.pdb
}

# top
alias topu='top -u $USER -d 1 -c'

# ls
alias lt='ls -lth' # sort by modified time
alias ll='ls -l'

# ambpdb in ambertools
# usage: pdb md.rs > md.pdb
alias pdb='ambpdb -p prmtop -c '

# conda
alias condaac='conda activate '
alias condade='conda deactivate'

# set notify
set -o notify

# do a new job when a job done
# usage: listen-wait <PID to wait> <cmd for the new job>
# eg: listen-wait 1234 ls -l
# could not use in nohup cmd, because nohup can only run program, not function
# if want to use in nohup, need to make a .sh file and source this part in the .sh file
function listen-wait() {
    local PID=$1
    shift
    local flag=1
    while [ "$flag" -eq 1 ]
    do
        sleep 1
        local PID_EXIST=$(ps -e | awk '{print $1}' | grep -w $PID)
        if [ ! $PID_EXIST ]; then
            flag=0
        fi
    done
    echo "PID: $PID done."
    $@
}

# solve the problem: ORCA parallel calc must be called with full path
# need to add orca in PATH and LD_LIBRARY_PATH for normal ORCA run
# usage: runorca <orca.inp> ...
# eg: runorca orca.inp > orca.log
function runorca() {
    $('which' orca) $@
}
