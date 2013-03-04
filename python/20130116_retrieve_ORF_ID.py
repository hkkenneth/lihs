# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 16-01-2013 
## Usage: python ~/code/python/20130116_retrieve_ORF_ID.py <SEQ ID LIST> <INPUT ORF ID LIST> <OUTPUT ORF ID LIST>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20130116_retrieve_ORF_ID.py to get usage'

set1 = set([])
for line in open(sys.argv[1], 'r'):
	set1.add(line[:-1])

outf = open(sys.argv[3], 'w')

for line in open(sys.argv[2], 'r'):
	seq_id = line[:line.rfind("_")]
	if seq_id in set1:
		outf.write(line)

outf.close()
