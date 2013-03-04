# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 31-01-2013
## Usage: python ~/code/python/042_ORF_IDs_list_append_seq_IDs.py <INPUT> <COL> <OUT>
## COL is 1-based

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/042_ORF_IDs_list_append_seq_IDs.py to get usage'

outf = open(sys.argv[3], 'w')
index = int(sys.argv[2])-1
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	seq_id = tokens[index][:tokens[index].rfind("_")]
	outf.write("%s\t%s\n" % (line[:-1], seq_id))
outf.close()
