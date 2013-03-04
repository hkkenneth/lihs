# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 12-11-2012 
## Usage: python ~/code/python/20121112_List_Append_Count.py <COUNT 1> <LEN> <ALL GOLD> <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 6:
        raise SystemExit, 'use grep "##" ~/code/python/20121107_List_Append_Counts.py to get usage'

count1 = {}
len_dict = {}
gold_set = set([])
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	count1[tokens[0]] = int(tokens[1])

for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

for line in open(sys.argv[3], 'r'):
	gold_set.add(line[:-1])

outf = open(sys.argv[5], 'w')

for line in open(sys.argv[4], 'r'):
	tokens = line[:-1].split("\t")
	seq_id = tokens[0][:(tokens[0].rfind("_"))]
	prot_id = tokens[2].split(" ")[0] 
	c1 = 0
	l = 0
	gold_str = ""
	if seq_id in count1:
		c1 = count1[seq_id]
	if seq_id in len_dict:
		l = len_dict[seq_id]
	if prot_id in gold_set:
		gold_str = "AlreadyInGold"
		
	outf.write("%s\t%i\t%i\t%s" % (gold_str, l, c1, line))

outf.close()
