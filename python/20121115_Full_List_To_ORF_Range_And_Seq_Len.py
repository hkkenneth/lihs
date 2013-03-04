# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 15-11-2012
## Usage: python ~/code/python/20121115_Full_List_To_ORF_Range_And_Seq_Len.py <INPUT> <LEN FILE> <ORF START> <ORF END> <ORF LEN> <LEN>

import sys
if len(sys.argv) < 7:
        raise SystemExit, 'use grep "##" ~/code/python/20121115_Full_List_To_ORF_Range_And_Seq_Len.py to get usage'

len_dict = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = tokens[1]

outf1 = open(sys.argv[3], 'w')
outf2 = open(sys.argv[4], 'w')
outf3 = open(sys.argv[5], 'w')
outf4 = open(sys.argv[6], 'w')

for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	orf_range = tokens[0][tokens[0].rfind("_")+1:].split("-")	
	outf1.write("%s\n" % orf_range[0])
	outf2.write("%s\n" % orf_range[1])
	outf3.write("%i\n" % ((abs(int(orf_range[0]) - int(orf_range[1])) + 1) / 3))
	outf4.write("%s\n" % len_dict[tokens[17]])

outf1.close()
outf2.close()
outf3.close()
outf4.close()

