# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 28-12-2012 
## Usage: python ~/code/python/029_Gene_Symbol_Ref_Updater.py <OLD VER> <MAPPING> <NEW VER>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/029_Gene_Symbol_Ref_Updater.py to get usage'

import string
newf = open(sys.argv[3], 'w')

mapping = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	mapping[tokens[0].upper()] = tokens[1].upper()
count = 0
for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	gs = tokens[3].upper()
	if gs in mapping:
		tokens[3] = mapping[gs]
		count += 1
		newf.write(string.join(tokens, "\t"))
	else:
		newf.write(line)

print "%i replacement done" % count
newf.close()
