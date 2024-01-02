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
