# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20130130_ORF_ID_to_Seq_ID.py <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20130130_ORF_ID_to_Seq_ID.py to get usage'

outf = open(sys.argv[2], 'w')
for line in open(sys.argv[1], 'r'):
	outf.write("%s\n" % line[:line.rfind("_")])
outf.close()
