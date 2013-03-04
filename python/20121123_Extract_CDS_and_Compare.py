# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 23-11-2012
## Usage: python ~/code/python/20121115_Find_CDS_Start.py <INPUT LIST> <ORF FASTA>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121115_Find_CDS_Start.py to get usage'

from Bio import SeqIO
import string

fasta_dict = {}
for r in SeqIO.parse(sys.argv[2], 'fasta'):
	fasta_dict[r.id] = str(r.seq)

outf = open(sys.argv[1] + ".with_cds", 'w')

for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	cds_start = int(tokens[18])
	seq = fasta_dict[tokens[0]]
	new_seq = seq[(cds_start-1):]
	outf.write("%s\t%s\n" % (string.join(tokens[:19], "\t"), str(new_seq)))
outf.close()
