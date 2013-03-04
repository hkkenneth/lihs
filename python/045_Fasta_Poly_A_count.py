# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/045_Fasta_Poly_A_count.py <INPUT FASTA>

import sys
if len(sys.argv) < 2:
        raise SystemExit, 'use grep "##" ~/code/python/045_Fasta_Poly_A_count.py to get usage'

from Bio import SeqIO

for r in SeqIO.parse(sys.argv[1], "fasta"):
	s = str(r.seq)
	s = s.replace("C", "X")
	s = s.replace("G", "X")
	s = s.replace("T", "X")
	tokens = s.split("X")
	max1 = 0
	for s1 in tokens:
		max1 = max(max1, len(s1))
	print "%s\t%i" % (r.id, max1)

