# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012
## Usage: python ~/code/python/20121102_Protein_ID_to_Def.py <REFERENCE FASTA> <PROTEIN ID> <OUTPUT>

from Bio import SeqIO
import sys

outf = open(sys.argv[3], 'w')

def_set = {}
for r in SeqIO.parse(sys.argv[1], "fasta"):
	def_set[r.id] = r.description

for line in open(sys.argv[2], 'r'):
	if line[:-1] in def_set:
		outf.write("%s\n" % def_set[line[:-1]])
	else:
		print "%s cannot be found in reference" % line[:-1]
outf.close()
