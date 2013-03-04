# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 15-02-2013
## Usage: python ~/code/python/20130215_Blat_Remove_Self.py <PSL FILE> <OUTPUT FILE>
## PSL FILE: output of BLAT without header

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20130215_Blat_Remove_Self.py to get usage'

outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	# self hit
	if tokens[9] == tokens[13]:
		continue
	if int(tokens[5]) + int(tokens[7]) > 10:
		continue
	if int(tokens[0]) < 100:
		continue
	outf.write(line)
outf.close()
