# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 05-11-2012
## Usage: python ~/code/python/20121105_BLASTP_List_Selection_4.py <INPUT LIST> <OUTPUT>

import sys

outf = open(sys.argv[2], 'w')
outf2 = open(sys.argv[2] + ".discarded", 'w')

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
	if tokens[2].find("Gold") >= 0:
		if (float(tokens[9]) / float(tokens[4]) > 0.5) and ( float(tokens[10]) / float(tokens[9]) > 0.5):
			flag = False
if flag:
	contig_set.add(seq)

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	seqid = tokens[0][:tokens[0].rfind("_")]
	if seqid in contig_set:
		outf.write(line)
	else:
		outf2.write(line)
outf.close()
