# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/_______.py <_________>

import sys
if len(sys.argv) < 2:
        raise SystemExit, 'use grep "##" ~/code/python/_________.py to get usage'

def parse(lines):
	for line in lines:
		tokens = line.split("\t")
		if (tokens[2] == "100.00") and (tokens[3] == "16"):
			return 1
	return 0

count = 0
lines = []
for line in open(sys.argv[1], 'r'):
	if line.find("# BLASTX 2.2.26+") == 0:
		count += parse(lines)
		lines = []
	if line.find("#") != 0:
		lines.append(line[:-1])
count += parse(lines)

print count
