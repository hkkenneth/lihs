# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 14-11-2012
## Usage: python ~/code/python/20121114_Blastp_List_Keep_Candidates.py <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121114_Blastp_List_Keep_Candidates.py to get usage'

def process_lines(lines, outf):
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
	for line in lines:
		tokens = line[:-1].split("\t")
		iden = int(tokens[9])
		seq_ID = tokens[0][:(tokens[0].rfind("_"))] 
		if max_iden == iden:
			outf.write("%s\t%s\n" % (line[:-1], seq_ID))
			continue
		iden_ratio = float(tokens[9]) / float(tokens[3])
		if max_iden_ratio == iden_ratio:
			outf.write("%s\t%s\n" % (line[:-1], seq_ID))
			continue
		diff = abs(int(tokens[8]) - int(tokens[3])) + int(tokens[11])
		if min_diff == diff:
			outf.write("%s\t%s\n" % (line[:-1], seq_ID))
			continue
		tar_range = tokens[7].split("-")
		tar_start = int(tar_range[0])
		if tar_start == 1:
			tar_end = float(tar_range[1])
			if tar_end / float(tokens[3]) >= 0.8:
				outf.write("%s\t%s\n" % (line[:-1], seq_ID))

orf_id = "XXX"
lines = []
outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	if tokens[0] == orf_id:
		lines.append(line)
	else:
		process_lines(lines, outf)
		orf_id = tokens[0]
		lines = [line]

outf.close()
