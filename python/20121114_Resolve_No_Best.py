# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 14-11-2012
## Usage: python ~/code/python/20121114_Resolve_No_Best.py <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121114_Resolve_No_Best.py to get usage'

def process_lines(lines, outf1, outf2):
	min_diff = 10000000
	max_iden = 0
	better_lines = []
	# preference goes to those having the first part aligned!
	for line in lines:
		tokens = line[:-1].split("\t")
		iden = int(tokens[9])
		tar_range = tokens[7].split("-")
		tar_start = int(tar_range[0])
		if tar_start == 1:
			tar_end = float(tar_range[1])
			if tar_end / float(tokens[3]) >= 0.8:
				better_lines.append(line)
				max_iden = max(max_iden, iden)
	# the head does not align...!
	if len(better_lines) == 0:
		for line in lines:
			tokens = line[:-1].split("\t")
			align_ratio = float(tokens[8]) / float(tokens[3])
			if (int(tokens[1]) >= int(tokens[3])) and (align_ratio > 0.8):
				better_lines.append(line)
				iden = int(tokens[9])
				max_iden = max(max_iden, iden)
		
	best_lines = []
	for line in better_lines:
		tokens = line[:-1].split("\t")
		iden = int(tokens[9])
		if max_iden == iden:
			best_lines.append(line)
	if len(best_lines) == 0:
		best_e = 1.0
		for line in lines:
			tokens = line[:-1].split("\t")
			best_e = min(best_e, float(tokens[5]))
		for line in lines:
			tokens = line[:-1].split("\t")
			if float(tokens[5]) < best_e + 1e-100:
				best_lines.append(line)
	min_gap = 10000
	if len(best_lines) > 1:
		new_best = []
		for line in best_lines:
			tokens = line.split("\t")
			min_gap = min(min_gap, int(tokens[11]))
		for line in best_lines:
			tokens = line.split("\t")
			if int(tokens[11]) == min_gap:
				new_best.append(line)
		best_lines = new_best
	if len(best_lines) == 1:
		outf1.write(best_lines[0])
	else:
		for line in best_lines:
			outf2.write(line)

seq_id = "XXX"
lines = []
outf1 = open(sys.argv[2] + ".resolve2.single_best", 'w')
outf2 = open(sys.argv[2] + ".resolve2.multi_best", 'w')

for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	if tokens[17] == seq_id:
		lines.append(line)
	else:
		process_lines(lines, outf1, outf2)
		seq_id = tokens[17]
		lines = [line]

outf1.close()
outf2.close()
