# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 22-11-2012
## Usage: python ~/code/python/20121122_Good_CDS_Remove_Same_CDS.py <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121122_Good_CDS_Remove_Same_CDS.py to get usage'

def process(lines, outf):
	if len(lines) == 0:
		return
	max_iden = 0
	max_count = 0
	best_line = ""
	for line in lines:
		tokens = line.split("\t")
		iden_minus_gaps = int(tokens[12]) - int(tokens[14])
		if iden_minus_gaps > max_iden:
			max_iden = iden_minus_gaps
			max_count = int(tokens[2])
			best_line = line
		elif max_iden == iden_minus_gaps:
			if int(tokens[2]) > max_count:
				max_count = int(tokens[2])
				best_line = line
			elif int(tokens[2]) == max_count:
				best_hit_len = int(best_line.split("\t")[6])
				if int(tokens[6]) < best_hit_len: # prefer shorter assignment
					best_line = line
	outf.write(best_line)
	
outf = open(sys.argv[2], 'w')

cds = "XX"
lines = []

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	this_cds = tokens[16]
	if this_cds == cds:
		lines.append(line)
	else:
		process(lines, outf)
		lines = [line]
		cds = this_cds
process(lines, outf)
outf.close()
