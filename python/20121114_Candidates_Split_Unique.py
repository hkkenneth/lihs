# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121114_Candidates_Split_Unique.py <INPUT> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121114_Candidates_Split_Unique.py to get usage'

outf1 = open(sys.argv[2] + ".uniqueHit", 'w')
outf2 = open(sys.argv[2] + ".multiHit.uniORF", 'w')
outf3 = open(sys.argv[2] + ".multiHit.multiORF", 'w')

seqID = "XXX"
lines = []
orf_set = set([])

for line in open(sys.argv[1], 'r'):
	seq_id = line[:-1].split("\t")[17]
	if seq_id != seqID:
		if len(lines) == 1:
			for l in lines:
				outf1.write(l)
		else:
			for l in lines:
				if len(orf_set) == 1:
					outf2.write(l)
				else:
					outf3.write(l)
		seqID = seq_id
		lines = []
		orf_set = set([])
	lines.append(line)
	orf_set.add(line.split("\t")[0])
	
outf1.close()
outf2.close()
outf3.close()
