#!python

# author: Yuhong LIN
# create date: 16:55, Dec 22, 2023

# plot data with cpptraj .dat output

import matplotlib.pyplot as plt
from glob import iglob

def plot_dat(file):
	with open(file, 'r') as f:
		f.readline()
		data = f.readlines()
	l = []
	for line in data:
		l.append(float(line.strip().split()[-1]))
	plt.figure(dpi = 300)
	plt.plot(l)
	plt.savefig(f'{file[:-4]}.png')
	plt.close()

def plot_cpptraj_dat(inp = r'./*.dat'):
	# default value: ./*.dat, when no param from call plot_cpptraj_dat() or '' as param from input()
	if len(inp) == 0:
		inp = r'./*.dat'
	for item in iglob(inp):
		plot_dat(item)

if __name__ == '__main__':
	inp = input('filename of cpptraj .dat file, [./*.dat]\n')
	plot_cpptraj_dat(inp)