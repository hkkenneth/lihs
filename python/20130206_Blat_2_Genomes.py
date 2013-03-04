# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 06-02-2013
## Usage: python ~/code/python/20130206_Blat_2_Genomes.py <BLAT INPUT> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20130206_Blat_2_Genomes.py to get usage'

outf = open(sys.argv[2] + ".py0206.internal", 'w')
outf2 = open(sys.argv[2] + ".py0206.internal.list", 'w')
outf5 = open(sys.argv[2] + ".py0206.internal.nick_big.list", 'w')
outf6 = open(sys.argv[2] + ".py0206.internal.ky_big.list", 'w')

#outf3 = open(sys.argv[2] + ".py0206.100+", 'w')
#outf4 = open(sys.argv[2] + ".py0206.100+.list", 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	if float(tokens[0]) / min(float(tokens[10]), float(tokens[14])) > 0.99:
		outf.write(line)
		outf2.write("%s\t%s\n" % (tokens[9], tokens[13]))
		if int(tokens[10]) > int(tokens[14]):
			outf5.write("%s\t%s\n" % (tokens[9], tokens[13]))
		else:
			outf6.write("%s\t%s\n" % (tokens[13], tokens[9]))

#	else:
#		if float(tokens[0]) > 100:
#			outf3.write(line)
#			outf4.write("%s\t%s\n" % (tokens[9], tokens[13]))
		

outf.close()
outf2.close()
outf5.close()
outf6.close()
