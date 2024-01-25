#!python

# author: Yuhong LIN
# create date: 14:44, 10 Jan, 2024

# create prepare file for amberMD to perform ALA scan

import os
from multiprocessing import Pool

def ala_scan_prepare(pdb_file, scan_list, leap_file = None, nprocs = None):
    def perform_ala_scan_prepare(item, leap_file = None):
        if os.path.exists(f'scan_{item}'):
            os.system(f'rm -r scan_{item}')
        os.mkdir(f'scan_{item}')
        cmd_line = f"cat {pdb_file} | awk '$5 != \"{item}\" || $3 == \"C\" || $3 == \"CA\" || $3 == \"N\"'"
        os.system(cmd_line)

        # use python to replace res name to ALA, maybe could use shell cmd to run faster, (Yuhong LIN)
        with open(f'scan_{item}', 'r') as f:
            file = f.readlines()
        for idx, line in enumerate(file):
            if file[:4] == 'ATOM':
                if line.strip().split()[4] == str(item):
                    file[idx] = line[:17] + 'ALA' + line[20:]
        with open(f'scan{item}', 'w') as f:
            f.write(''.join(file))

        if leap_file:
            os.chdir(f'scan_{item}')
            os.system('tleap -f ../leap.in')
            os.chdir('../')

    if nprocs:
        pool = Pool(nprocs)
        for item in scan_list:
            pool.apply_async(func = perform_ala_scan_prepare, args = (item, leap_file))
        pool.close()
        pool.join()
        
    else:
        for item in scan_list:
            perform_ala_scan_prepare(item, leap_file)