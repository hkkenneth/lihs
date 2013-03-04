# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 30-11-2012
## Usage: python ~/code/python/024_Protein_Fasta_Select_M.py <INPUT> <OUTPUT WITH M> <OUTPUT WITHOUT M>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/004_Fasta_Find_Identical_Seq.py to get usage'

from Bio import SeqIO

out1 = open(sys.argv[2], 'w')
out2 = open(sys.argv[3], 'w')

for r in SeqIO.parse(sys.argv[1], "fasta"):
	if str(r.seq)[0] == "M":
		SeqIO.write(r, out1, "fasta")
	else:
		SeqIO.write(r, out2, "fasta")

out1.close()
out2.close()
