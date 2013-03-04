# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 27-11-2012
## Usage: python ~/code/python/20121127_Table_To_ORF_Fasta.py <INPUT LIST> <OUTPUT FASTA> <ORF FASTA>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121127_Table_To_ORF_Fasta.py to get usage'

from Bio import SeqIO
import string

fasta_dict = {}
for r in SeqIO.parse(sys.argv[3], 'fasta'):
	fasta_dict[r.id] = r

outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	cds_start = int(tokens[18])
	r = fasta_dict[tokens[0]]
	r.description += "(CDS_start:" + tokens[18] + ")"
	SeqIO.write(r[(cds_start-1):], outf, "fasta")
outf.close()
