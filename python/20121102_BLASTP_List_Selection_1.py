# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 05-11-2012
## Usage: python ~/code/python/20121102_BLASTP_List_Selection_1.py <INPUT> <OUTPUT> <CUTOFF>

import sys

outf = open(sys.argv[2], 'w')
cutoff = float(sys.argv[3])

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	sbj_start = int(tokens[7].split("-")[0])
	sbj_end = int(tokens[7].split("-")[1])
	hit_len = int(tokens[3])
	if (sbj_start == 1) and (float(sbj_end) / hit_len >= cutoff):
		outf.write(line)
outf.close()
