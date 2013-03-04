# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 05-11-2012
## Usage: python ~/code/python/20121102_BLASTP_List_Selection_2.py <INPUT> <OUTPUT> <IDENTITIES CUTOFF> <POSITIVES CUTOFF>

import sys

outf = open(sys.argv[2], 'w')
i_cutoff = float(sys.argv[3])
p_cutoff = float(sys.argv[4])

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	posi = float(tokens[10])
	iden = float(tokens[9])
	align_len = float(tokens[8])
	if (iden / align_len >= i_cutoff) and (posi / align_len >= p_cutoff):
		outf.write(line)
outf.close()
