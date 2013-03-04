# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 22-11-2012
## Usage: python ~/code/python/20121121_Split_Lines_To_New_Old.py.py <GOLD STANDARD DETAILS> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121121_Split_Lines_To_New_Old.py to get usage'

old_iden = {}
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	if tokens[0] == "":
		continue
	old_iden[tokens[0]] = int(tokens[1])

outf1 = open(sys.argv[2] + ".new", 'w')
outf2 = open(sys.argv[2] + ".better", 'w')
outf3 = open(sys.argv[2] + ".old", 'w')

for line in open(sys.argv[2], 'r'):
	tokens = line.split("\t")
	id = tokens[5].split(" ")[0]
	iden = int(tokens[12])
	if id in old_iden:
		if old_iden[id] >= iden:
			outf3.write(line)
		else:
			outf2.write(line)
	else:
		outf1.write(line)

outf1.close()
outf2.close()
