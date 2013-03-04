# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121213_CDS_ID_To_Transcript_ID.py <IN> <OUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121213_CDS_ID_To_Transcript_ID.py to get usage'

outf = open(sys.argv[2], 'w')
for line in open(sys.argv[1], 'r'):
	outf.write("%s\n" % line[:line.rfind("_")])
outf.close()
