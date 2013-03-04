# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/_______.py <_________>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/_________.py to get usage'

def process(lines, outf, outf2, outf3):
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
		seq_dict = {}
		for line in full_lines:
			tokens = line.split("\t")
			seq = tokens[16]
			if seq in seq_dict:
				seq_dict[seq].append(line)
			else:
				seq_dict[seq] = [line]
		for k in seq_dict.keys():
			best_line = ""
			max_count = 0
			for line in seq_dict[k]:
				tokens = line.split("\t")
				count = int(tokens[2])
				if count > max_count:
					best_line = line
			if len(seq_dict.keys()) == 1:
				outf.write(best_line)
			else:
				outf2.write(best_line)
			
	else:
		for line in lines:
			outf3.write(line)

		
	
outf = open(sys.argv[2], 'w')
outf2 = open(sys.argv[3], 'w')
outf3 = open(sys.argv[4], 'w')

prot_id = "XX"
lines = []

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	this_prot_id = tokens[5].split(" ")[0]
	if this_prot_id == prot_id:
		lines.append(line)
	else:
		process(lines, outf, outf2, outf3)
		lines = [line]
		prot_id = this_prot_id
process(lines, outf, outf2, outf3)
outf.close()
outf2.close()
outf3.close()
