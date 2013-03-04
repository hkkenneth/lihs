# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 23-11-2012 
## Usage: python ~/code/python/20121123_List_Select_Unique_CDS.py <INPUT LIST WITH CDS SEQ> <OUTPUT PREFIX> <COUNT>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121123_List_Select_Unique_CDS.py to get usage'

count_dict = {}
for line in open(sys.argv[3], 'r'):
	tokens = line[:-1].split("\t")
	count_dict[tokens[0]] = int(tokens[1])

cds_dict = {}

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	cds = tokens[19]
	if cds not in cds_dict:
		cds_dict[cds] = []
	cds_dict[cds].append(tokens[17])

outf1 = open(sys.argv[2] + ".uniq", 'w')
outf2 = open(sys.argv[2] + ".dup", 'w')
logf = open(sys.argv[2] + ".log", 'w')
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	cds = tokens[19]
	if len(cds_dict[cds]) == 1:
		outf1.write(line)
	else:
		max_count = 0
		max_id = ""
		for ids in cds_dict[cds]:
			if ids in count_dict:
				if count_dict[ids] > max_count:
					max_count = count_dict[ids]
					max_id = ids
		if max_id == tokens[17]:
			outf1.write(line)
		elif max_id == "":
			logf.write("%s.... no count info, so use %s\n" % (tokens[19][:20], cds_dict[cds][0]))
			if cds_dict[cds][0] == tokens[17]:
				outf1.write(line)
			else:
				outf2.write(line)
		else:
			outf2.write(line)
			

outf1.close()
outf2.close()
logf.close()
