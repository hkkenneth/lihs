# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121128_Assign_Gene_Symbol_To_Table.py <GENE SYMBOL REF> <OUTPUT> <XML...>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121128_Assign_Gene_Symbol_To_Table.py to get usage'

symbols = {}
for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	symbols[tokens[1]] = tokens[3].upper()

outf = open(sys.argv[2], 'w')

from Bio import SeqIO
from Bio.Blast import NCBIXML

for s in sys.argv[3:]:
	for record in NCBIXML.parse(open(s, 'r')):
		q_id = record.query.split(" ")[0]
		if len(record.alignments) == 0:
			outf.write("%s\t_________\n" % q_id)
		else:
			gi = record.alignments[0].hit_def.split(" ")[0].split("|")[1]
			if gi in symbols:
				outf.write("%s\t%s\n" % ( q_id, symbols[gi]))
			else:
				outf.write("%s\t_________\n" % q_id)

outf.close()
