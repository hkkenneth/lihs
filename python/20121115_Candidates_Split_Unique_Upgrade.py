# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121115_Candidates_Split_Unique_Upgrade.py <INPUT>

import sys
if len(sys.argv) < 2:
        raise SystemExit, 'use grep "##" ~/code/python/20121115_Candidates_Split_Unique_Upgrade.py to get usage'

outf1 = open(sys.argv[1] + ".uniqueHit", 'w')
outf2 = open(sys.argv[1] + ".multiHit.uniORF", 'w')
outf3 = open(sys.argv[1] + ".multiHit.multiORF", 'w')

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
		good_lines = []
		for l in lines:
			if l.split("\t")[0] in good_set:
				good_lines.append(l)

		if len(good_lines) == 1:
			for l in good_lines:
				outf1.write(l)
		else:
			for l in good_lines:
				if len(good_set) == 1:
					outf2.write(l)
				else:
					outf3.write(l)
		seqID = seq_id
		lines = []
		the_max_ratio = 0.0
		orf_dict = {}
	orf_id = tokens[0]
	lines.append(line)
	ratio = float(tokens[8]) / float(tokens[3])
	if orf_id in orf_dict:
		orf_dict[orf_id] = max(orf_dict[orf_id], ratio)
	else:
		orf_dict[orf_id] = ratio
	the_max_ratio = max(the_max_ratio, ratio)
	
good_set = set([])
for k in orf_dict.keys():
	if orf_dict[k] >= the_max_ratio * 0.7:
		good_set.add(k)
good_lines = []
for l in lines:
	if l.split("\t")[0] in good_set:
		good_lines.append(l)

if len(good_lines) == 1:
	for l in good_lines:
		outf1.write(l)
else:
	for l in good_lines:
		if len(good_set) == 1:
			outf2.write(l)
		else:
			outf3.write(l)
	
outf1.close()
outf2.close()
outf3.close()

