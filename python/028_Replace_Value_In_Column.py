# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/028_Replace_Value_In_Column.py <REPLACEMENT LIST> <COLUMN> <INPUT> <OUTPUT>
## column index is 1-based

import sys
import string
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/028_Replace_Value_In_Column.py to get usage'

rep_dict = {}
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	rep_dict[tokens[0]] = tokens[1]

col = int(sys.argv[2]) - 1

outf = open(sys.argv[4], 'w')
replace_count = 0
for line in open(sys.argv[3], 'r'):
	tokens = line[:-1].split("\t")
	if tokens[col] in rep_dict:
		tokens[col] = rep_dict[tokens[col]]
		replace_count += 1
	outf.write("%s\n" % string.join(tokens, "\t"))
outf.close()

print "Number of replacement: %i" % replace_count
