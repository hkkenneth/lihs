# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 14-11-2012
## Usage: python ~/code/python/20121114_Blastp_List_Keep_Candidates.py <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121114_Blastp_List_Keep_Candidates.py to get usage'

def process_lines(lines, outf1, outf2, outf3, outf4):
	min_diff = 10000000
	max_iden = 0
	max_iden_ratio = 0.0
	for line in lines:
		tokens = line[:-1].split("\t")
		diff = abs(int(tokens[8]) - int(tokens[3])) + int(tokens[11]) # plus gap to penalize gap
		iden = int(tokens[9])
		iden_ratio = float(tokens[9]) / float(tokens[3])
		max_iden = max(max_iden, iden)
		max_iden_ratio = max(max_iden_ratio, iden_ratio)
		min_diff = min(min_diff, diff)
	best = []
	for line in lines:
		tokens = line[:-1].split("\t")
		iden = int(tokens[9])
		iden_ratio = float(tokens[9]) / float(tokens[3])
		diff = abs(int(tokens[8]) - int(tokens[3])) + int(tokens[11])
		tar_range = tokens[7].split("-")
		tar_start = int(tar_range[0])
		tar_end = float(tar_range[1])
		if (tar_start == 1) and (tar_end / float(tokens[3]) >= 0.8) and (max_iden == iden) and (max_iden_ratio == iden_ratio) and (min_diff == diff):
			best.append(line)
	if len(best) == 0:
		for line in lines:
			outf4.write(line)
	else:
		if len(best) == 1:
			for line in best:
				outf1.write(line)
		else:
			for line in best:
				outf3.write(line)
		for line in lines:
			if line not in best:
				outf2.write(line)

seq_id = "XXX"
lines = []
outf1 = open(sys.argv[2] + ".best", 'w')
outf2 = open(sys.argv[2] + ".not_best", 'w')
outf3 = open(sys.argv[2] + ".multi_best", 'w')
outf4 = open(sys.argv[2] + ".no_best", 'w')

for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	if tokens[17] == seq_id:
		lines.append(line)
	else:
		process_lines(lines, outf1, outf2, outf3, outf4)
		seq_id = tokens[17]
		lines = [line]

outf1.close()
outf2.close()
outf3.close()
outf4.close()
