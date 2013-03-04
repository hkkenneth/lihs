# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012
## Usage: python ~/code/python/006_Fasta_Find_Internal.py <INPUT FASTA> <OUTPUT PREFIX>
## Output file: <OUTPUT PREFIX>.python006.list <OUTPUT PREFIX>.python006.log
## For each sequence in the FASTA FILE, it and its reverse complement is 
## compared with other sequence to check whether internal sequences exist.
## Output format: one or more lines are output for each sequence with duplicates.
## The first column is the sequence id of first occurence, the second column is subsequent occurence
## Useful commands:

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/006_Fasta_Find_Internal.py to get usage'

from Bio import SeqIO

outf = open(sys.argv[2] + ".python006.list" , 'w')
logf = open(sys.argv[2] + ".python006.log" , 'w')
seq_dict = {}
id_list = []

for r in SeqIO.parse(sys.argv[1], "fasta"):
	seq_dict[r.id] = str(r.seq)
	id_list.append(r.id)

dup_set = set([])

for i in xrange(len(id_list)):
	id = id_list[i]
	if id in dup_set:
		continue
	seq1 = seq_dict[id]
	for other_id in id_list[(i+1):]:
		if other_id in dup_set:
			continue
		seq2 = seq_dict[other_id]
		if (len(seq1) > len(seq2)) and (seq2 in seq1):
			dup_set.add(other_id)
		if (len(seq2) > len(seq1)) and (seq1 in seq2):
			dup_set.add(id)
			break
for dup in dup_set:
	outf.write("%s\n" % dup)

outf.close()
logf.close()
