# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 08-01-2013
## Usage: python ~/code/python/031_Blastp_List_Select_By_Contig_ID.py <IN> <CONTIG ID> <OUT>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/031_Blastp_List_Select_By_Contig_ID.py to get usage'

the_set = set([])
for line in open(sys.argv[2], 'r'):
	the_set.add(line[:-1])

outf = open(sys.argv[3], 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	id = tokens[0]
	if id[:id.rfind("_")] in the_set:
		outf.write(line)
outf.close()
