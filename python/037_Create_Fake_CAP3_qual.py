# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 22-01-2013
## Usage: python ~/code/python/037_Create_Fake_CAP3_qual.py <INPUT> <Qual>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/037_Create_Fake_CAP3_qual.py to get usage'

outf = open(sys.argv[1] + ".qual", 'w')
for line in open(sys.argv[1], 'r'):
	if line.startswith(">"):
		outf.write(line)
	else:
		for c in line:
			if c == "\n":
				outf.write(c)
			else:
				outf.write("%s " % sys.argv[2])
outf.close()
