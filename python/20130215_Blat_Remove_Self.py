# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 15-02-2013
## Usage: python ~/code/python/20130215_Blat_Remove_Self.py <PSL FILE> <OUTPUT FILE>
## PSL FILE: output of BLAT without header

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20130215_Blat_Remove_Self.py to get usage'

outf = open(sys.argv[2], 'w')

skip = 0
for line in open(sys.argv[1], 'r'):
	if line.startswith("psLayout"):
		skip = 5
	if skip > 0:
		skip -= 1
		outf.write(line)
		continue
	tokens = line.split("\t")
	# self hit
	if tokens[9] == tokens[13]:
		continue
	outf.write(line)
outf.close()
