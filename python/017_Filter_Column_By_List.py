# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 22-11-2012 
## Usage: python ~/code/python/017_Filter_Column_By_List.py <ID LIST> <COLUMN> <IN LIST OUTPUT> <OUT LIST OUTPUT> <INPUT FILES ...>
## COLUMN is 1-based

import sys
if len(sys.argv) < 6:
        raise SystemExit, 'use grep "##" ~/code/python/017_Filter_Column_By_List.py to get usage'

name_set = set([])
for line in open(sys.argv[1], 'r'):
	name_set.add(line[:-1])

if sys.argv[3] == "-":
	f1 = None
else:
	f1 = open(sys.argv[3], 'w')

if sys.argv[4] == "-":
	f2 = None
else:
	f2 = open(sys.argv[4], 'w')

index = int(sys.argv[2]) - 1

for s in sys.argv[5:]:
	for line in open(s, 'r'):
		tokens = line[:-1].split("\t")
		if tokens[index] in name_set:
			if f1 is not None:
				f1.write(line)
		elif f2 is not None:
			f2.write(line)
if f1 is not None:
	f1.close()
if f2 is not None:
	f2.close()
