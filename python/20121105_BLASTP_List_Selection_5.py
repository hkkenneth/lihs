# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 05-11-2012
## Usage: python ~/code/python/20121105_BLASTP_List_Selection_5.py <INPUT LIST> <OUTPUT>

import sys

outf = open(sys.argv[2], 'w')

best_set = set([])

seq = "XXXX"
flag = False
contig_set = set([])
tie_set_all = set([])
tie_set = set([])
maxLine = ""
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	seqid = tokens[0][:tokens[0].rfind("_")]
	if seqid != seq:
		best_set.add(maxLine)
		seq = seqid
		maxIdenP = 0.0
		maxLine = ""
		tie_set_all = tie_set_all.union(tie_set)
		tie_set = set([])
	iden = float(tokens[10]) / float(tokens[4])
	if iden > maxIdenP:
		maxIdenP = iden
		maxLine = tokens[0] + tokens[3]
		tie_set = set([])
	elif iden > maxIdenP * 0.97:
		tie_set.add(tokens[0] + tokens[3])

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	seqid = tokens[0][:tokens[0].rfind("_")]
	prot_id = tokens[3].split(" ")[0]
	i = line.find(prot_id)
	start = int(tokens[8].split("-")[0])
	gold_str = ""
	if (tokens[0] + tokens[3]) in best_set:
		if start == 1:
			gold_str = "AutoGold"
		else:
			gold_str = "AutoPreGold"
	elif (tokens[0] + tokens[3]) in tie_set_all:
		gold_str = "AutoTieGold"
	outf.write("%s%s\t%s" % (line[:i], gold_str, line[i:]))
		
outf.close()
