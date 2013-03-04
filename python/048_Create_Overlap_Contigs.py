# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/048_Create_Overlap_Contigs.py <OUTPUT> <LEN CUTOFF> <PIECE SIZE> <OVERLAP> <INPUT FILES...>

import sys
if len(sys.argv) < 6:
        raise SystemExit, 'use grep "##" ~/code/python/048_Create_Overlap_Contigs.py to get usage'

from Bio import SeqIO

cutoff = int(sys.argv[2])
piece_size = int(sys.argv[3])
overlap = int(sys.argv[4])

if cutoff < piece_size:
	print "Cutoff cannot be smaller than Piece Size"
	exit()

if overlap >= piece_size:
	print "Overlap cannot be larger than Piece Size"
	exit()

outf = open(sys.argv[1], 'w')

count = 0
for s in sys.argv[5:]:
	for rec in SeqIO.parse(s, "fasta"):
		if len(rec.seq) < cutoff:
			rec.description = "" 
			SeqIO.write(rec, outf, "fasta")
			continue
		start = 0
		end = piece_size
		while start <= len(rec.seq):
			r = rec[start:end]
			count += 1
			r.id = str(count) + "_" + r.id + "_" + str(start) + "-" + str(end)
			r.description = ""
			SeqIO.write(r, outf, "fasta")
			start = end - overlap
			if end == len(rec.seq):
				start = len(rec.seq) + 1
			end = min(start + piece_size, len(rec.seq))
outf.close()
