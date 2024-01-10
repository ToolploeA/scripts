#!python

# author: Yuhong LIN
# create date: 14:44, 10 Jan, 2024

# create prepare file for amberMD to perform ALA scan

# still in development !!!

import os
from multiprocessing import Pool

def ala_scan_prepare(pdb_file, scan_list, leap_file = None, nprocs = None):
    def perform_ala_scan_prepare(item, leap_file = None):
        if os.path.exists(f'scan_{item}'):
            os.system(f'rm -r scan_{item}')
        os.mkdir(f'scan_{item}')
        cmd_line = f"cat {pdb_file} | awk '$5 != \"{item}\" || $3 == \"C\" || $3 == \"CA\" || $3 == \"N\"'"
        os.system(cmd_line)
        if leap_file:
            os.chidr(f'scan_{item}')
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