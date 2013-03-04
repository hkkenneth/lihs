# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 09-11-2012
## Usage: python ~/code/python/013_Count_To_Freq.py <INPUT> <OUTPUT>

import sys

count_dict = {}
outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	l = int(tokens[1])
	if l in count_dict:
		count_dict[l] += 1
	else:
		count_dict[l] = 1

ks = count_dict.keys()
ks.sort()
for k in ks:
	outf.write("%i\t%i\n" % (k, count_dict[k]))
outf.close()
