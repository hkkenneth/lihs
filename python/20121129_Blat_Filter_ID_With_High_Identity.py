# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121129_Blat_Filter_ID_With_High_Identity.py <BLAT RESULT> <QUERY ID OUTPUT> <PERCENT IDENTITY CUTOFF>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121129_Blat_Filter_ID_With_High_Identity.py to get usage'

def set_to_file(set1, f):
	for s in set1:
		f.write("%s\n" % s)
	f.close()

high_set = set([])
count = 0
for line in open(sys.argv[1], 'r'):
	count += 1
	if count <= 5:
		continue
	tokens = line.split("\t")
	iden = float(tokens[0])
	q_size = min(float(tokens[10]), float(tokens[14]))
	if (iden / q_size) >= float(sys.argv[3]):
		high_set.add(tokens[9])

set_to_file(high_set, open(sys.argv[2], 'w'))
