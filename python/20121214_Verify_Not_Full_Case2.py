# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121214_Verify_Not_Full_Case2.py <INPUT>

import sys
if len(sys.argv) < 2:
        raise SystemExit, 'use grep "##" ~/code/python/20121214_Verify_Not_Full_Case2.py to get usage'

count = 0
case2_count = 0
for line in open(sys.argv[1], 'r'):
	count += 1
	tokens = line.split("\t")
	range = tokens[7].split("-")
	if int(range[1]) == int(tokens[3]):
		case2_count += 1

print count
print case2_count
