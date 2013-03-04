# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121218_Size_Stat_Summarizer.py <INPUT>

import sys
if len(sys.argv) < 2:
        raise SystemExit, 'use grep "##" ~/code/python/20121218_Size_Stat_Summarizer.py to get usage'

range = [0, 1, 3, 5, 10, 30, 50, 100, 300]
range_dict = {}
for i in range:
	range_dict[i] = 0
total = 0
for line in open(sys.argv[1], 'r'):
	tokens = line.strip().split(" ")
	total += int(tokens[0])
	for r in range:
		if abs(int(tokens[1])) <= r:
			range_dict[r] += int(tokens[0])

for r in range:
	print "+-%i\t%i\t%s" % (r, range_dict[r], str(range_dict[r]/float(total))[:5])
print "Total:\t%i" % total
