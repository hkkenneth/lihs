# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 07-11-2012 
## Usage: python ~/code/python/20121107_List_Append_Counts.py <COUNT 1> <COUNT 2> <LEN> <ALL GOLD> <GOLD 6> <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 8:
        raise SystemExit, 'use grep "##" ~/code/python/20121107_List_Append_Counts.py to get usage'

count1 = {}
count2 = {}
len_dict = {}
gold_set = set([])
gold_6_set = set([])
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	count1[tokens[0]] = int(tokens[1])

for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	count2[tokens[0]] = int(tokens[1])

for line in open(sys.argv[3], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

for line in open(sys.argv[4], 'r'):
	gold_set.add(line[:-1])

for line in open(sys.argv[5], 'r'):
	gold_6_set.add(line[:(line.rfind("_c"))])

outf = open(sys.argv[7], 'w')

for line in open(sys.argv[6], 'r'):
	tokens = line[:-1].split("\t")
	seq_id = tokens[0][:(tokens[0].rfind("_"))]
	comp_id = seq_id[:seq_id.rfind("_c")]
	prot_id = tokens[2].split(" ")[0] 
	c1 = 0
	c2 = 0
	l = 0
	gold_str = ""
	gold_6_str = ""
	if seq_id in count1:
		c1 = count1[seq_id]
	if seq_id in count2:
		c2 = count2[seq_id]
	if seq_id in len_dict:
		l = len_dict[seq_id]
	if prot_id in gold_set:
		gold_str = "AlreadyInGold"
	if comp_id in gold_6_set:
		gold_6_str = "InGold6"
		
	outf.write("%s\t%s\t%i\t%i\t%i\t%s" % (gold_6_str, gold_str, l, c1, c2, line))

outf.close()
