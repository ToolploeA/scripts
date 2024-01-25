#!python

# author: Yuhong LIN
# cerate date: 18:40, Jan 3, 2024

# sth for protein process

import os
import shutil


def one2three(s):
    # s: str, 1-letter code for residue
    # return: str, 3-letter code

    one2three_dict = {'V':'VAL', 'I':'ILE', 'L':'LEU', 'E':'GLU', 'Q':'GLN', 'D':'ASP', 'N':'ASN', 'H':'HIS', 'W':'TRP', 'F':'PHE', 'Y':'TYR', 'R':'ARG', 'K':'LYS', 'S':'SER', 'T':'THR', 'M':'MET', 'A':'ALA', 'G':'GLY', 'P':'PRO', 'C':'CYS'}

    return one2three_dict[s]

def three2one(s):
    # s: str, 3-letter code for residue
    # return: str, 1-letter code

    three2one_dict = {'VAL':'V', 'ILE':'I', 'LEU':'L', 'GLU':'E', 'GLN':'Q', 'ASP':'D', 'ASN':'N', 'HIS':'H', 'TRP':'W', 'PHE':'F', 'TYR':'Y', 'ARG':'R', 'LYS':'K', 'SER':'S', 'THR':'T', 'MET':'M', 'ALA':'A', 'GLY':'G', 'PRO':'P', 'CYS':'C'}

    return three2one_dict[s]

def mutation(pdb_file, mutant_idx, residue, result_file):
    # pdb_file: str, path to pdb file
    # mutant_idx: int or list of int, index of residue to be mutated
    # residue: str or list of str, 3-letter code for residue
    # result_file: str, path to result file

    # mutate
    if type(mutant_idx) == int:
        mutant_idx = [mutant_idx]
        residue = [residue]
    shutil.copy(pdb_file, 'tmp.pdb')
    for idx in mutant_idx:
        cmd_line = f"cat tmp.pdb | awk '$5 != \"{idx}\" || $3 == \"C\" || $3 == \"CA\" || $3 == \"N\"' > tmp.pdb"
        os.system(cmd_line)
    with open('tmp.pdb', 'r') as f:
        pdb_lines = f.readlines()
    for idx, line in enumerate(pdb_lines):
        if line[:4] == 'ATOM':
            if int(line.strip().split()[4]) in mutant_idx:
                pdb_lines[idx] = line[:17] + residue[mutant_idx.index(int(line.strip().split()[4]))] + line[20:]
    
    # write result
    result = open(result_file, 'w')
    result.writelines(pdb_lines)
    result.close()


if __name__ == '__main__':
    # testing

    print(one2three('S'))
    print(three2one('TYR'))