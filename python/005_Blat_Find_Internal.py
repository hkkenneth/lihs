# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012 
## Usage: python ~/code/python/005_Blat_Find_Internal.py <PSL FILE> <OUTPUT LIST> > <STDOUT>
## PSL FILE: output of BLAT without header
## OUTPUT LIST: list of contig id of sequences contained in another contig
## STDOUT: pairs of exact match
## Useful commands:

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/005_Blat_Find_Internal.py to get usage'

removef = open(sys.argv[2], 'w')
removef_d = open(sys.argv[2] + ".detail", 'w')
remove_set = set([])

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	# self hit
	if tokens[9] == tokens[13]:
		continue
	if int(tokens[4]) + int(tokens[6]) > 0:
		continue
	match = int(tokens[0])
	len1 = int(tokens[10])
	len2 = int(tokens[14])
	if match == min(len1, len2):
		removef_d.write(line)
		if len1 < len2:
			remove_set.add(tokens[9])
		elif len2 < len1:
			remove_set.add(tokens[13])
		else:
			print "%s\t%s" % (tokens[9], tokens[13])
for k in remove_set:
	removef.write("%s\n" % k)

removef.close()
removef_d.close()
