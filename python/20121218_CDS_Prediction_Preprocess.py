# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 20-12-2012 
## Usage: python ~/code/python/20121218_CDS_Prediction_Preprocess.py <INPUT> <OUTPUT>
## Select a best hit for a contig to continue with the rest of processing

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121218_CDS_Prediction_Preprocess.py to get usage'

seq_line_dict = {}
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	seq_id = tokens[0][:tokens[0].rfind("_")]
	if seq_id in seq_line_dict:
		seq_line_dict[seq_id].append(line)
	else:
		seq_line_dict[seq_id] = [line]

outf = open(sys.argv[2], 'w')

for k in seq_line_dict.keys():
	best_line = seq_line_dict[k][0]
	for line in seq_line_dict[k]:
		tokens = line[:-1].split("\t")
		bt = best_line[:-1].split("\t")
		score = int(tokens[9])*2 + int(tokens[10]) - int(tokens[11]) - int(tokens[3])
		bscore = int(bt[9])*2 + int(bt[10]) - int(bt[11]) - int(bt[3])
		if score > bscore:
			best_line = line
	outf.write(best_line)

outf.close()
