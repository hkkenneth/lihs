# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 20-12-2012
## Usage: python ~/code/python/20121220_Has_Stop_Or_Not.py <INPUT> <LEN FILE>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121220_Has_Stop_Or_Not.py to get usage'

outf1 = open(sys.argv[1] + ".stop", 'w')
outf2 = open(sys.argv[1] + ".no_stop", 'w')

len_dict = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	has_stop = True
	orf = tokens[0]
	range = orf[orf.rfind("_")+1:].split("-")
	if int(range[0]) < int(range[1]):
		if int(range[1]) + 3 > len_dict[orf[:orf.rfind("_")]]:
			has_stop = False
	elif int(range[1]) < 4:
		has_stop = False
	if has_stop:
		outf1.write(line)
	else:
		outf2.write(line)	

outf1.close()
outf2.close()
