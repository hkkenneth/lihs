# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012
## Usage: python ~/code/python/008_Bowtie_Count_Hits.py <BOWTIE OUTPUT> <COUNT OUTPUT FILE>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/008_Bowtie_Count_Hits.py to get usage'

rdict = {}
outf = open(sys.argv[2], 'w')
for line in open(sys.argv[1], 'r'):
	id = line.split("\t")[2]
	if id in rdict:
		rdict[id] += 1
	else:
		rdict[id] = 1
for k in rdict.keys():
	outf.write("%s\t%i\n" % (k, rdict[k]))
outf.close()

