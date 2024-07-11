#!python

# author: Yuhong LIN
# create date: 21:35, Jan 3, 2024

# read prmtop, prmcrd file from tleap, and other file from molecular science

import fortranformat as ff
import numpy as np
from math import ceil

atomic_number_to_symbol = {
    1: "H",
    2: "He",
    3: "Li",
    4: "Be",
    5: "B",
    6: "C",
    7: "N",
    8: "O",
    9: "F",
    10: "Ne",
    11: "Na",
    12: "Mg",
    13: "Al",
    14: "Si",
    15: "P",
    16: "S",
    17: "Cl",
    18: "Ar",
    19: "K",
    20: "Ca",
    21: "Sc",
    22: "Ti",
    23: "V",
    24: "Cr",
    25: "Mn",
    26: "Fe",
    27: "Co",
    28: "Ni",
    29: "Cu",
    30: "Zn",
    31: "Ga",
    32: "Ge",
    33: "As",
    34: "Se",
    35: "Br",
    36: "Kr",
    37: "Rb",
    38: "Sr",
    39: "Y",
    40: "Zr",
    41: "Nb",
    42: "Mo",
    43: "Tc",
    44: "Ru",
    45: "Rh",
    46: "Pd",
    47: "Ag",
    48: "Cd",
    49: "In",
    50: "Sn",
    51: "Sb",
    52: "Te",
    53: "I",
    54: "Xe",
    55: "Cs",
    56: "Ba",
    57: "La",
    58: "Ce",
    59: "Pr",
    60: "Nd",
    61: "Pm",
    62: "Sm",
    63: "Eu",
    64: "Gd",
    65: "Tb",
    66: "Dy",
    67: "Ho",
    68: "Er",
    69: "Tm",
    70: "Yb",
    71: "Lu",
    72: "Hf",
    73: "Ta",
    74: "W",
    75: "Re",
    76: "Os",
    77: "Ir",
    78: "Pt",
    79: "Au",
    80: "Hg",
    81: "Tl",
    82: "Pb",
    83: "Bi",
    84: "Po",
    85: "At",
    86: "Rn",
    87: "Fr",
    88: "Ra",
    89: "Ac",
    90: "Th",
    91: "Pa",
    92: "U",
    93: "Np",
    94: "Pu",
    95: "Am",
    96: "Cm",
    97: "Bk",
    98: "Cf",
    99: "Es",
    100: "Fm",
    101: "Md",
    102: "No",
    103: "Lr",
    104: "Rf",
    105: "Db",
    106: "Sg",
    107: "Bh",
    108: "Hs",
    109: "Mt",
    110: "Ds",
    111: "Rg",
    112: "Cn",
    113: "Nh",
    114: "Fl",
    115: "Mc",
    116: "Lv",
    117: "Ts",
    118: "Og"
}

symbol_to_atomic_number = {v: k for k, v in atomic_number_to_symbol.items()}

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

def read_xyz(filename, num_element = False):
    with open(filename, 'r') as f:
        n_atom = int(f.readline().strip())
        f.readline()
        lines = f.readlines()
    if num_element:
        element = [atomic_number_to_symbol[int(line.split()[0])] for line in lines]
    else:
        element = [line.split()[0] for line in lines]
    coord = np.array([[float(line.split()[1]), float(line.split[2]), float(line.split[3])] for line in lines])
    return {
        'coord': coord,
        'element': element,
        'n_atom': n_atom
    }

def write_xyz(filename, coord, element, n_atoms = None, num_element = False):
    if num_element:
        element = [symbol_to_atomic_number[x] for x in element]
    if not n_atoms:
        n_atoms = len(element)
    with open(filename, 'w') as f:
        f.write(f'{n_atoms}\n\n')
        for idx in range(len(element)):
            f.write(f'{element[idx]} {coord[idx][0]} {coord[idx][1]} {coord[idx][2]}\n')
        

def read_multi_xyz(filename, sep = None, num_element = False):
    with open(filename, 'r') as f:
        all_lines = f.readlines()
    n_atoms = int(all_lines[0].strip())
    n_struc = len(all_lines) // (n_atoms + 2)
    coord_pool = []
    if sep:
        n_lines_sep = len(sep.split('\n'))
    for struc_idx in range(n_struc):
        lines = all_lines[struc_idx * (n_atoms + 2 + n_lines_sep): (struc_idx + 1) * (n_atoms + 2 + n_lines_sep)]
        if struc_idx == 0:
            if num_element:
                element = [atomic_number_to_symbol[int(line.split()[0])] for line in lines]
            else:
                element = [line.split()[0] for line in lines]
        coord = np.array([[float(line.split()[1]), float(line.split[2]), float(line.split[3])] for line in lines])
        coord_pool.append(coord)
    coord_pool = np.array(coord_pool)
    return {
        'coord': coord_pool,
        'element': element,
        'n_atoms': n_atoms
    }

def write_multi_xyz(filename, element, coord, n_atoms = None, sep = None, num_element = False):
    if num_element:
        element = [symbol_to_atomic_number[x] for x in element]
    if not n_atoms:
        n_atoms = len(element)
    with open(filename, 'w') as f:
        for struc_idx in range(coord.shape[0]):
            f.write(f'{n_atoms}\n\n')
            for atom_idx in range(n_atoms):
                f.write(f'{element[atom_idx]} {coord[struc_idx][atom_idx][0]} {coord[struc_idx][atom_idx][1]} {coord[struc_idx][atom_idx][2]}\n')
            if sep:
                f.write(sep)
    