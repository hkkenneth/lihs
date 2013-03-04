# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 30-Nov-2012 
## Usage: python ~/code/python/20121130_Ensemble_Genbank_Dump_Parser.py <GENE BANK INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121130_Ensemble_Genbank_Dump_Parser.py to get usage'

gene_sym = ""

outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1], 'r'):
	if line.startswith("ACCESSION"):
		outf.write("--------------------\n")
	elif line.startswith("                     /locus_tag"):
		gene_sym = line.split('"')[1]
		outf.write("%s\n" % gene_sym.upper())

outf.close()
