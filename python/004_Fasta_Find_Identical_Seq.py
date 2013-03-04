# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012
## Usage: python ~/code/python/004_Fasta_Find_Identical_Seq.py <INPUT FASTA> <OUTPUT PREFIX>
## Output file: <OUTPUT PREFIX>.python004.list <OUTPUT PREFIX>.python004.log
## For each sequence in the FASTA FILE, it and its reverse complement is 
## compared with other sequence to check whether duplicate sequences exist
## Output format: one or more lines are output for each sequence with duplicates.
## The first column is the sequence id of first occurence, the second column is subsequent occurence
## Useful commands:
## cut -f 1 output | sort | uniq | wc -l
## cut -f 2 output > duplicate_contig_id

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/004_Fasta_Find_Identical_Seq.py to get usage'

from Bio import SeqIO

outf = open(sys.argv[2] + ".python004.list" , 'w')
logf = open(sys.argv[2] + ".python004.log" , 'w')
seq_dict = {}

dup_count = 0
rev_dup_count = 0
count = 0

for r in SeqIO.parse(sys.argv[1], "fasta"):
	count += 1
	seq = str(r.seq)
	if seq in seq_dict:
		seq_dict[seq].append(r.id)
		dup_count += 1
	else:
		revseq = str(r.seq.reverse_complement())
		if revseq in seq_dict:
			seq_dict[revseq].append(r.id)
			rev_dup_count += 1
		else:
			seq_dict[seq] = [r.id]

ks = seq_dict.keys()
logf.write("Total sequences in fasta: %i\n" % count)
logf.write("Total unique sequences: %i\n" % len(ks))
logf.write("Total duplicate sequences: %i\n" % dup_count)
logf.write("Total duplicate sequences in reverse complement: %i\n" % rev_dup_count)

for k in ks:
	if len(seq_dict[k]) > 1:
		for s in seq_dict[k][1:]:
			outf.write("%s\t%s\n" % (seq_dict[k][0], s))
outf.close()
logf.close()
