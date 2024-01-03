#!python

# author: Yuhong LIN
# create date: 16:55, Dec 22, 2023

# plot data with cpptraj .dat output

import matplotlib.pyplot as plt

def plot(file):
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

filename = input('filename of cpptraj .dat file:\n')
plot(filename)
