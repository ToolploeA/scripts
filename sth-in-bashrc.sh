#!/bin/bash

# get .pdb file in RCSB with PDB ID
# use: getpdb 2HAC
function getpdb() {
    wget files.rcsb.org/download/$1.pdb
}

# top
alias topu='top -u $USER -d 1 -c'

# ls
alias lt='ls -lth'
alias ll='ls -l'

# ambpdb in ambertools
# use: pdb md.rs > md.pdb
alias pdb='ambpdb -p prmtop -c '

# conda
alias condaac='conda activate '
alias condade='conda deactivate'

# set notify
set -o notify

# do a new job when a job done
# use: listen-wait <PID to wait> <cmd for the new job>
# eg: listen-wait 1234 ls -l
function listen-wait() {
    local PID=$1
    shift
    local flag=1
    local result=1
    while [ "$flag" -eq 1 ]
    do
        sleep 1
        local PID_EXIST=$(ps -u | awk '{print $2}' | grep -w $PID)
        if [ ! $PID_EXIST ]; then
            flag=0
        fi
    done
    echo "PID: $PID done."
    $@
}