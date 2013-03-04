# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/_______.py <PREFIX> <ASSIGNMENT> <PY 032 RESULTS>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/_________.py to get usage'

translate_dict = {}
gs_dict = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	translate_dict[tokens[1].split(" ")[0]] = tokens[0].upper()
	gs_dict[tokens[0].upper()] = 0

#outf = open(sys.argv[1], 'w')

count = 0
for s in sys.argv[3:]:
	for line in open(s, 'r'):
		count += 1
		tokens = line.split("\t")
		id = tokens[2].split(" ")[0]
		if id in translate_dict:
			gs_dict[translate_dict[id]] += 1

for k in gs_dict.keys():
	print "%s\t%i" % (k, gs_dict[k])

print "Total: %i" % count
