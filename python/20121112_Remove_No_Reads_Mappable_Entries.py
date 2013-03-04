# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 07-11-2012 
## Usage: python ~/code/python/20121112_Remove_No_Reads_Mappable_Entries.py <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121112_Remove_No_Reads_Mappable_Entries.py to get usage'


outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	if tokens[4] == "0":
		continue
	outf.write(line)

outf.close()
