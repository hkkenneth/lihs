# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/_______.py <_________>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/_________.py to get usage'

def process(lines, outf, outf2):
	if len(lines) == 0:
		return
	has_full = False
	full_lines = []
	max_iden = 0
	for line in lines:
		tokens = line.split("\t")
		s_range = tokens[10].split("-")
		prot_len = float(tokens[6])
		if (int(s_range[0]) == 1) and (float(s_range[1]) / prot_len > 0.9):
			has_full = True
			full_lines.append(line)
			max_iden = max(max_iden, int(tokens[12]))
	if has_full:
		best_line = "\n"
		max_count = 0
		for line in full_lines:
			tokens = line.split("\t")
			count = int(tokens[2])
			if max_count < count:
				max_count = count
				best_line = line
		outf.write(best_line)
	else:
		for line in lines:
			outf2.write(line)

		
	
outf = open(sys.argv[2], 'w')
outf2 = open(sys.argv[3], 'w')

prot_id = "XX"
lines = []

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	this_prot_id = tokens[5].split(" ")[0]
	if this_prot_id == prot_id:
		lines.append(line)
	else:
		process(lines, outf, outf2)
		lines = [line]
		prot_id = this_prot_id
