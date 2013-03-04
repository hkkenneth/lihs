# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 05-11-2012
## Usage: python ~/code/python/20121102_BLASTP_List_Selection_1.py <INPUT LIST SMALLER> <INPUT LIST BIGGER> <GOLD STANDARD ID LIST> <OUTPUT>

import sys

gold_set = set([])
for line in open(sys.argv[3], 'r'):
	gold_set.add(line[:-1])

outf = open(sys.argv[4], 'w')

seq = "XXXX"
flag = False
contig_set = set([])
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	seqid = tokens[0][:tokens[0].rfind("_")]
	if seqid != seq:
		if flag:
			contig_set.add(seq)
		flag = True
		seq = seqid
	if tokens[2].split(" ")[0] in gold_set:
		flag = False
if flag:
	contig_set.add(seq)

for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	seqid = tokens[0][:tokens[0].rfind("_")]
	if seqid in contig_set:
		outf.write(line)
outf.close()
