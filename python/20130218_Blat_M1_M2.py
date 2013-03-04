# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 18-02-2013
## Usage: python ~/code/python/20130218_Blat_M1_M2.py <BLAT INPUT> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20130218_Blat_M1_M2.py to get usage'

outf = open(sys.argv[2] + ".py0218." + "ky.replace_list", 'w')
outf2 = open(sys.argv[2] + ".py0218." + "nick.replace_list", 'w')
outf3 = open(sys.argv[2] + ".py0218." + "ky.replace_list.details", 'w')
outf4 = open(sys.argv[2] + ".py0218." + "nick.replace_list.details", 'w')

line_dict = {}

detail1 = set([])
detail2 = set([])

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	k = tokens[9] + tokens[13]
	if k not in line_dict:
		line_dict[k] = []
	line_dict[k].append(line)

	if (float(tokens[0]) - float(tokens[5]) - float(tokens[7])) / min(float(tokens[14]), float(tokens[10])) > 0.99:
		if int(tokens[10]) > int(tokens[14]):
			outf2.write("%s\t%s\n" % (tokens[9], tokens[13] ))
			detail2.add(k)
		else:
			outf.write("%s\t%s\n" % (tokens[13], tokens[9] ))
			detail1.add(k)

for k in detail1:
	for line in line_dict[k]:
		outf3.write(line)

for k in detail2:
	for line in line_dict[k]:
		outf4.write(line)

outf.close()
outf2.close()
outf3.close()
outf4.close()
