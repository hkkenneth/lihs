# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 14-11-2012 
## Usage: python ~/code/python/20121114_Resolve_Multi_ORF.py <INPUT> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121114_Resolve_Multi_ORF.py to get usage'

outf1 = open(sys.argv[2] + ".ORF_resolved", 'w')
outf2 = open(sys.argv[2] + ".ORF_not_resolved", 'w')

seqID = "XXX"
lines = []
orf_dict = {}
the_max_ratio = 0.0

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	seq_id = tokens[17]
	if seq_id != seqID:
		good_set = set([])
		for k in orf_dict.keys():
			if orf_dict[k] >= the_max_ratio * 0.7:
				good_set.add(k)
		if len(good_set) == 1:
			for l in lines:
				if l.split("\t")[0] in good_set:
					outf1.write(l)
		else:
			for l in lines:
				if l.split("\t")[0] in good_set:
					outf2.write(l)
		seqID = seq_id
		the_max_ratio = 0.0
		lines = []
		orf_dict = {}
	orf_id = tokens[0]
	lines.append(line)
	ratio = float(tokens[8]) / float(tokens[3])
	if orf_id in orf_dict:
		orf_dict[orf_id] = max(orf_dict[orf_id], ratio)
	else:
		orf_dict[orf_id] = ratio
	the_max_ratio = max(the_max_ratio, orf_dict[orf_id])
	
outf1.close()
outf2.close()
