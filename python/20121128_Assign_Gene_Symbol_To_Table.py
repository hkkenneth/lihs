# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121128_Assign_Gene_Symbol_To_Table.py <INPUT TABLE> <GENE SYMBOL REF> <OUTPUT>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121128_Assign_Gene_Symbol_To_Table.py to get usage'

symbols = {}
for line in open(sys.argv[2], 'r'):
	tokens = line.split("\t")
	symbols[tokens[1]] = tokens[3]

outf = open(sys.argv[3], 'w')
manf = open(sys.argv[3] + ".manual", 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	gi = tokens[2].split(" ")[0].split("|")[1]
	if gi in symbols:
		outf.write("%s\t%s\n" % (line[:-1], symbols[gi].upper()))
	else:
		manf.write(line)

outf.close()
manf.close() 
	
