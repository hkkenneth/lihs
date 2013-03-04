# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 25-11-2012 
## Usage: python ~/code/python/20121112_List_Append_Count.py <COUNT> <LEN> <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/20121107_List_Append_Counts.py to get usage'

count1 = {}
count2 = {}
len_dict = {}
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	count1[tokens[0]] = int(tokens[1])
	c_name = tokens[0][:tokens[0].rfind("_")]
	if c_name in count2:
		count2[c_name] += int(tokens[1])
	else:
		count2[c_name] = int(tokens[1])

for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

outf = open(sys.argv[4], 'w')

for line in open(sys.argv[3], 'r'):
	tokens = line[:-1].split("\t")
	seq_id = tokens[0][:(tokens[0].rfind("_"))]
	c_id = seq_id[:seq_id.rfind("_")]
	c1 = 0
	c2 = 0
	l = 0
	gold_str = ""
	if seq_id in count1:
		c1 = count1[seq_id]
		c2 = count2[c_id]
	if seq_id in len_dict:
		l = len_dict[seq_id]
		
	outf.write("%s\t%i\t%i\t%i\n" % (line[:-1], c2, c1, l))

outf.close()
