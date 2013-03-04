# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 17-12-2012
## Usage: python ~/code/python/20121217_Find_Best_E.py <INPUT> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121217_Find_Best_E.py to get usage'

outf1 = open(sys.argv[2] + ".per_seq", 'w')
outf2 = open(sys.argv[2] + ".per_orf", 'w')
outf3 = open(sys.argv[2] + ".per_sym", 'w')

seq_dict = {}
sym_dict = {}

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	id = tokens[0][:tokens[0].rfind("_")]
	if id not in seq_dict:
		seq_dict[id] = {}
	if tokens[0] not in seq_dict[id]:
		seq_dict[id][tokens[0]] = float(tokens[5])
	else:
		seq_dict[id][tokens[0]] = min(seq_dict[id][tokens[0]], float(tokens[5]))
	if (len(tokens) > 17):
		sym = tokens[17].upper()
		if sym not in sym_dict:
			sym_dict[sym] = 1.0
		sym_dict[sym] = min(sym_dict[sym], float(tokens[5]))
	
for k in seq_dict.keys():
	minE = 1.0
	for k2 in seq_dict[k].keys():
		outf2.write("%s\t%s\n" % (k2, str(seq_dict[k][k2])))
		minE = min(minE, seq_dict[k][k2])
	outf1.write("%s\t%s\n" % (k, str(minE)))
for k in sym_dict.keys():
	outf3.write("%s\t%s\n" % (k, str(sym_dict[k])))

outf1.close()
outf2.close()
outf3.close()
