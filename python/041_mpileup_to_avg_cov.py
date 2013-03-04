# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/041_mpileup_to_avg_cov.py <MPILEUP FILE> <GENOME SIZE> <RANGE> <OUTPUT>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/041_mpileup_to_avg_cov.py to get usage'

dict1 = {}
for i in range(int(sys.argv[2])):
	dict1[i+1] = 0

sum = 0
for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	dict1[int(tokens[1])] = int(tokens[3])
	sum += int(tokens[3])

outf = open(sys.argv[4], 'w')
for line in open(sys.argv[3], 'r'):
	tokens = line[:-1].split("\t")
	s = int(tokens[0])
	e = int(tokens[1])
	total = 0
	for i in range(e-s+1):
		total += dict1[s+i]
	outf.write("%i\n" % total)
outf.write("Sum:\t%i\n" % sum)

outf.close()
