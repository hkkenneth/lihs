# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 24-01-2013
## Usage: python ~/code/python/039_Fasta_ID_Remove_Dot.py <IN> <OUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/039_Fasta_ID_Remove_Dot.py to get usage'


outf = open(sys.argv[2], 'w')
for line in open(sys.argv[1], 'r'):
	if line.startswith(">"):
		outf.write(line.replace(".", "-"))
	else:
		outf.write(line)
outf.close()
