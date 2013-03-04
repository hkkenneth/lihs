# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 17-01-2013
## Usage: python ~/code/python/034_Fasta_Realign.py <INPUT> <LEN> <OUTPUT>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/034_Fasta_Realign.py to get usage'

l = int(sys.argv[2])
outf = open(sys.argv[3], 'w')
seq = ""
for line in open(sys.argv[1], 'r'):
	if line[0] == ">" :
		if len(seq) >= 1:
			index = 0
			while index < len(seq):
				outf.write("%s\n" % seq[index:min(index + l, len(seq))])
				index += l
		outf.write(line)
		seq = ""
	else:
		seq = seq + line[:-1]
if len(seq) >= 1:
	index = 0
	while index < len(seq):
		outf.write("%s\n" % seq[index:min(index + l, len(seq))])
		index += l
outf.close()
