# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 20-11-2012
## Usage: python ~/code/python/20121120_Combine_DogHumanMouse_To_Gold.py <DOG COMBINED> <HUMAN COMBINED> <MOUSE COMBINED> <CONTIG ID> <MULTI ORF>
# cut -f 18 00dog/gold_to_dog.py010.20121114.out.group_by_seqID.multiHit.multiORF.ORF_not_resolved 0[1-2]*/*multiORF | sort | uniq > ALL_MULTI_ORF
# python ~/code/python/20121120_Combine_DogHumanMouse_To_Gold.py 00dog/FINAL_combined 01human/FINAL_combined 02mouse/FINAL_combined FINAL_CONTIG_ID ALL_MULTI_ORF
# paste FINAL_GOLD_COL 20121120_out > 20121120_out.txt 

import sys
if len(sys.argv) < 6:
        raise SystemExit, 'use grep "##" ~/code/python/20121120_Combine_DogHumanMouse_To_Gold.py to get usage'

multi_orf_set = set([])
for line in open(sys.argv[5], 'r'):
	multi_orf_set.add(line[:-1])

dog_dict = {}
human_dict = {}
mouse_dict = {}
for line in open(sys.argv[1], 'r'):
	id = line.split("\t")[0]
	dog_dict[id] = string.join(line[:-1].split("\t")[5:], "\t")
for line in open(sys.argv[2], 'r'):
	id = line.split("\t")[0]
	human_dict[id] = string.join(line[:-1].split("\t")[5:], "\t")
for line in open(sys.argv[3], 'r'):
	id = line.split("\t")[0]
	mouse_dict[id] = string.join(line[:-1].split("\t")[5:], "\t")

outf = open("20121120_out", 'w')
logf = open("20121120_out.log", 'w')

for line in open(sys.argv[4], 'r'):
	id = line[:-1]
	d_str = "\t\t\t\t\t\t"
	h_str = "\t\t\t\t\t\t"
	m_str = "\t\t\t\t\t\t"
	has_something = False
	percent = 0.0
	assignment = ""
	if id in dog_dict:
		d_str = dog_dict[id]
		tokens = d_str.split("\t")
		if float(tokens[9])/float(tokens[7]) > percent:
			percent = float(tokens[9])/float(tokens[7])
			assignment = d_str	
		has_something = True
	if id in human_dict:
		h_str = human_dict[id]
		tokens = h_str.split("\t")
		percent = max(percent, float(tokens[9])/float(tokens[7]))
		has_something = True
	if id in mouse_dict:
		m_str = mouse_dict[id]
		tokens = m_str.split("\t")
		percent = max(percent, float(tokens[9])/float(tokens[7]))
		has_something = True
	outf.write("%s\t\t%s\t\t%s\t\t%s\n" % (id, d_str, h_str, m_str))
	if has_something:
		if percent < 0.5:
			logf.write("%s has low identity: %s\n" % (id, str(percent)))
	elif id not in multi_orf_set:
			logf.write("%s has no assignment\n" % id)
	
logf.close()
outf.close()
