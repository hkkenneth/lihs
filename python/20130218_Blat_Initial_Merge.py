# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 18-02-2013
## Usage: python ~/code/python/20130218_Blat_Initial_Merge.py <BLAT INPUT> <OUTPUT PREFIX> <CUTOFF>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20130218_Blat_Initial_Merge.py to get usage'

outf = open(sys.argv[2] + ".py0218." + sys.argv[3] + ".internal", 'w')
outf2 = open(sys.argv[2] + ".py0218." + sys.argv[3] + ".ky_can_use", 'w')
outf3 = open(sys.argv[2] + ".py0218." + sys.argv[3] + ".ky_check", 'w')

ky_dict = {}
ky_use_set = {}
cutoff = int(sys.argv[3])

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	if tokens[13] not in ky_dict:
		ky_dict[tokens[13]] = set([])
	if int(tokens[0]) >= cutoff:
		ky_dict[tokens[13]].add(tokens[9])
	if int(tokens[10]) >= int(tokens[14]):
		continue
	if (float(tokens[0]) - float(tokens[5]) - float(tokens[7])) / float(tokens[10]) > 0.99:
	#if float(tokens[0]) / float(tokens[10]) > 0.99:
		outf.write(line)
		if tokens[13] not in ky_use_set:
			ky_use_set[tokens[13]] = set([])
		ky_use_set[tokens[13]].add(tokens[9])

for k in ky_use_set.keys():
	if len(ky_dict[k] - ky_use_set[k]) == 0:
	#if len(ky_use_set[k]) == 1:
		for k2 in ky_use_set[k]:
			outf2.write("%s\t%s\n" % (k2, k ))
	else:
		for k2 in ky_use_set[k]:
			outf3.write("%s\t%s\n" % (k2, k ))

outf.close()
outf2.close()
outf3.close()
