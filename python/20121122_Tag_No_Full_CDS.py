# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 22-11-2012 
## Usage: python ~/code/python/20121122_Tag_No_Full_CDS.py <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121122_Tag_No_Full_CDS.py to get usage'

outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	s_range = tokens[10].split("-")
	q_range = tokens[9].split("-")
	prot_len = float(tokens[6])
	orf_len = float(tokens[4])
	tag_str = "INCOMPLETE\t%s" % str(float(tokens[11]) / prot_len)
	if (int(q_range[0]) == 1) and (q_range[1] == tokens[4]):
		tag_str = "FRAGMENT_FULL\t%s" % str(float(tokens[4]) / prot_len)
	if float(int(s_range[1]) - int(s_range[0])) / prot_len >= 0.9:
		if int(q_range[0]) >= int(s_range[0]):
			tag_str = "DIFF_HEAD\t%s" % str(float(tokens[11]) / prot_len)
		else:
			tag_str = "HIGH_COV_SHORT\t%s" % str(int(q_range[0]) - int(s_range[1]))
	outf.write("%s\t%s\n" % (line[:-1], tag_str))
outf.close()
