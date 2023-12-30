#!/bin/bash


# get .pdb file in RCSB with PDB ID
# use: getpdb 2HAC
function getpdb() {
    wget files.rcsb.org/download/$1.pdb
}
