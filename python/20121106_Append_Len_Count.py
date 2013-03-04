# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 20-11-2012 
## Usage: python ~/code/python/20121106_Append_Len_Count.py <LEN> <COUNT> <IN> <OUT>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/20121106_Append_Len_Count.py to get usage'

len_dict = {}
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

count_dict = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	count_dict[tokens[0]] = int(tokens[1])

outf = open(sys.argv[4], 'w')

for line in open(sys.argv[3], 'r'):
	tokens = line.split("\t")
	i = tokens[0].rfind("_")
	id = tokens[0][:i]
	seq_group = tokens[0].split("seq")[0]
	l = 0
	c = 0
	if id in len_dict:
		l = len_dict[id]
	if id in count_dict:
		c = count_dict[id]
	outf.write("%s\t%i\t%i\t%s" % (seq_group, l, c, line))

outf.close()
