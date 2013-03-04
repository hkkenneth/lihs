# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/_______.py <_________>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/_________.py to get usage'

outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	if tokens[2] != "0":
		outf.write(line)

outf.close()
