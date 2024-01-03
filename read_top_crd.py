#!python

# author: Yuhong LIN
# create date: 21:35, Jan 3, 2024

# read prmtop, prmcrd file from tleap

import fortranformat as ff
import numpy as np
from math import ceil

def read_fortran_fmt(content, format, shape = None):
    # content: list of str, cut from readlies()
    # format: str, %FORAMT in prmtop, eg: '(5E16.8)
    # shape: tuple, reshape
    reader = ff.FortranRecordReader(format)
    con = [reader.read(line) for line in content]
    con = np.array(con).flatten()
    con = con[con != None]
    if shape:
        con = con.reshape(shape)
    return con

def read_prmtop(filename):
    with open(filename, 'r') as f:
        file = f.readlines()
    flag_name = []
    flag_idx_a = []
    flag_idx_b = []
    flag_fmt = []
    for idx, line in enumerate(file):
        if r'%FLAG' in line:
            if r'%FORMAT' in file[idx + 1]:
                flag_fmt.append(file[idx + 1][7:].strip())
                flag_idx_a.append(idx + 2)
                flag_idx_b.append(idx)
            else:
                flag_fmt.append(file[idx + 2][7:].strip())
                flag_idx_a.append(idx + 3)
                flag_idx_b.append(idx)
            flag_name.append(line[6:].strip())
    flag_idx_b = flag_idx_b[1:]
    prmtop_data = {}
    for i in range(len(flag_idx_a)):
        if i != len(flag_idx_a) - 1:
            con = file[flag_idx_a[i]:flag_idx_b[i]]
        else:
            con = file[flag_idx_a[i]:]
        con = read_fortran_fmt(con, flag_fmt[i])
        prmtop_data[flag_name[i]] = con
    return prmtop_data

def read_prmcrd(filename):
    fmt = '(6E12.7)'
    with open(filename, 'r') as f:
        f.readline()
        num = int(f.readline().strip())
        file = f.readlines()
    coord = read_fortran_fmt(file[:ceil(num / 2)], fmt, shape = (num, 3))
    return coord
