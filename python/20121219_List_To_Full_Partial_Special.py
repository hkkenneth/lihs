# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 19-12-2012 
## Usage: python ~/code/python/20121219_List_To_Full_Partial_Special.py <INPUT>

import sys
if len(sys.argv) < 2:
        raise SystemExit, 'use grep "##" ~/code/python/20121219_List_To_Full_Partial_Special.py to get usage'

outf1 = open(sys.argv[1] + ".full", 'w') 
outf2 = open(sys.argv[1] + ".partial", 'w') 
outf3 = open(sys.argv[1] + ".special", 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	if tokens[7].startswith("1-") and tokens[14].startswith("M"):
		outf1.write(line)
	elif tokens[6].startswith("1-"):
		outf2.write(line)
	else:
		outf3.write(line)

outf1.close()
outf2.close()
outf3.close()
