# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 09-12-2012
## Usage: python ~/code/python/026_Protein_Fasta_Select_X.py <INPUT> <OUTPUT WITH X> <OUTPUT WITHOUT X>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/026_Protein_Fasta_Select_X.py to get usage'

from Bio import SeqIO

out1 = open(sys.argv[2], 'w')
out2 = open(sys.argv[3], 'w')

for r in SeqIO.parse(sys.argv[1], "fasta"):
	if str(r.seq).find("X") >= 0:
		SeqIO.write(r, out1, "fasta")
	else:
		SeqIO.write(r, out2, "fasta")

out1.close()
out2.close()
