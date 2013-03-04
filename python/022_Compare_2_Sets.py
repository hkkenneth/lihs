# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/022_Compare_2_Sets.py <SET A INPUT> <SET B INPUT> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/022_Compare_2_Sets.py to get usage'

def file_to_set(f):
	set1 = set([])
	for line in open(f, 'r'):
		set1.add(line[:-1])
	return set1

def set_to_file(set1, f):
	for s in set1:
		f.write("%s\n" % s)
	f.close()

seta = file_to_set(sys.argv[1])
setb = file_to_set(sys.argv[2])

outf1 = open(sys.argv[3] + ".set_AB", 'w')
outf2 = open(sys.argv[3] + ".set_A_only", 'w')
outf3 = open(sys.argv[3] + ".set_B_only", 'w')

set_to_file((seta & setb), outf1)
set_to_file((seta - setb), outf2)
set_to_file((setb - seta), outf3)
