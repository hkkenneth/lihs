# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 14-11-2012
## Usage: python ~/code/python/20121114_Candidates_Resolve_Duplicate_References.py <DUPLICATE REF> <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121114_Candidates_Resolve_Duplicate_References to get usage'

def process_lines(lines, outf1, outf2, logf, duplicate_dict):
	if len(lines) == 0:
		return
	first_prot = lines[0].split("\t")[2].split(" ")[0]
	seq_id = lines[0][:-1].split("\t")[17]
	all_same = True
	prots_str = ""
	for line in lines[1:]:
		this_prot = lines[0].split("\t")[2].split(" ")[0]
		if first_prot not in duplicate_dict:
			all_same = False
			break
		if this_prot not in duplicate_dict[first_prot]:
			all_same = False
			break
		prots_str = prots_str + "," + this_prot
	if all_same:
		logf.write("%s\t%s\tRepresented\t%s\n" % (seq_id, first_prot, prots_str[1:]))
		outf1.write(lines[0])
	else:
		for line in lines:
			outf2.write(line)
	

duplicate_dict = {}
origin_ks = set([])
for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	if tokens[0] not in duplicate_dict:
		duplicate_dict[tokens[0]] = set([tokens[0]])
		origin_ks.add(tokens[0])
	duplicate_dict[tokens[0]].add(tokens[1])

for k in origin_ks:
	for k2 in duplicate_dict[k]:
		duplicate_dict[k2] = duplicate_dict[k]

seq_id = "XXX"
lines = []
outf1 = open(sys.argv[3] + ".same", 'w')
outf2 = open(sys.argv[3] + ".not_same", 'w')
logf = open(sys.argv[3] + ".same.log", 'w')

for line in open(sys.argv[2]):
	tokens = line[:-1].split("\t")
	if tokens[17] == seq_id:
		lines.append(line)
	else:
		process_lines(lines, outf1, outf2, logf, duplicate_dict)
		seq_id = tokens[17]
		lines = [line]

outf1.close()
outf2.close()
logf.close()
