# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 28-Nov-2012 
## Usage: python ~/code/python/021_GeneBank_To_Gene_Symbol_List.py <GENE BANK INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/021_GeneBank_To_Gene_Symbol_List.py to get usage'

is_def = False
def_str = ""
gi = ""
ref = ""
gene_sym = ""

outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1], 'r'):
	if line.startswith("DEFINITION"):
		is_def = True
	elif line.startswith("ACCESSION"):
		is_def = False
	elif line.startswith("VERSION"):
		temp = line[12:-1]
		ref = temp[:temp.find(" ")]
		gi = temp.split("GI:")[1]
	elif line.startswith("                     /gene="):
		gene_sym = line.split('"')[1]
		outf.write("gi|%s|ref|%s|\t%s\t%s\t%s\t%s\n" % (gi, ref, gi, ref, gene_sym, def_str))
		def_str = ""
	if is_def:
		def_str = def_str + line[12:-1]

outf.close()
