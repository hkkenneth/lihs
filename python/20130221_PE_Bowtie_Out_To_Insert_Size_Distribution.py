# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20130221_PE_Bowtie_Out_To_Insert_Size_Distribution.py <IN> <OUT> <OFFSET>
## INPUT = BOWTIE
## OFFSET is needed to correct the insert size
## OFFSET should be READ LEN + TOTAL 5'-end trimmed bases

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20130221_PE_Bowtie_Out_To_Insert_Size_Distribution.py to get usage'

outf = open(sys.argv[2], 'w')
count = 0
a = 0
b = 0
offset=int(sys.argv[3])
for line in open(sys.argv[1], 'r'):
	count +=1
	tokens = line[:-1].split("\t")
	if count % 2 == 1:
		a = int(tokens[3])
	else:
		b = int(tokens[3])
		outf.write("%s\t%i\n" % (tokens[0][:tokens[0].find("/")], abs(a-b)+offset))
outf.close()
