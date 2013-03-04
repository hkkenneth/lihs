# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/_______.py <LIST> <VALUE FILE> <COL FOR LIST> <COL TO ADD>
## COL are 1-based

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/_________.py to get usage'

set1 = set([])
for line in open(sys.argv[1], 'r'):
	set1.add(line[:-1])

index1 = int(sys.argv[3])-1
index2 = int(sys.argv[4])-1

sum = 0
value_count = 0
for line in open(sys.argv[2], 'r'):
	tokens = line.split("\t")
	if tokens[index1] in set1:
		value_count += 1
		sum += int(tokens[index2])

print "%i values sum to %i" % (value_count, sum)
