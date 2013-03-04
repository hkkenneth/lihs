# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 06-12-2012
## Usage: python ~/code/python/20121206_454_Read_Status_Chimeric_Freq_Count.py <_________>

import sys
if len(sys.argv) < 2:
        raise SystemExit, 'use grep "##" ~/code/python/20121206_454_Read_Status_Chimeric_Freq_Count.py to get usage'

set_dict = {}

outf = open(sys.argv[1] + ".summary", 'w')
outf2 = open(sys.argv[1] + ".one_ref_only", 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	if tokens[0] not in set_dict:
		set_dict[tokens[0]] = set([])
	set_dict[tokens[0]].add(tokens[4])

count_dict = {}

for k in set_dict.keys():
	count = len(set_dict[k])
	if count == 1:
		outf2.write("%s\n" % k)
	if count in count_dict:
		count_dict[count] += 1
	else:
		count_dict[count] = 1

outf.write("%s\n" % str(count_dict))
outf.close()
outf2.close()
