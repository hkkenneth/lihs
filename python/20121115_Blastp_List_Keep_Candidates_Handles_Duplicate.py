# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 15-11-2012
## Usage: python ~/code/python/20121115_Blastp_List_Keep_Candidates_Handles_Duplicate.py <DUPLICATE REF> <INPUT> <OUTPUT>
# cat ~/code/python/20121114_Blastp_List_Keep_Candidates.py ~/code/python/20121114_Candidates_Resolve_Duplicate_References.py > ~/code/python/20121115_Blastp_List_Keep_Candidates_Handles_Duplicate.py

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121115_Blastp_List_Keep_Candidates_Handles_Duplicate.py to get usage'

def process_lines(lines, outf, logf, duplicate_dict):
	if len(lines) == 0:
		return
	min_diff = 10000000
	max_iden = 0
	max_iden_ratio = 0.0
	# find the best criteria first
	for line in lines:
		tokens = line[:-1].split("\t")
		diff = abs(int(tokens[8]) - int(tokens[3])) + int(tokens[11]) # plus gap to penalize gap
		iden = int(tokens[9])
		iden_ratio = float(tokens[9]) / float(tokens[3])
		max_iden = max(max_iden, iden)
		max_iden_ratio = max(max_iden_ratio, iden_ratio)
		min_diff = min(min_diff, diff)
	list_of_candidates = []
	for line in lines:
		tokens = line[:-1].split("\t")
		prot_id = tokens[2].split(" ")[0]
		seq_ID = tokens[0][:(tokens[0].rfind("_"))] 
		if prot_id in duplicate_dict:
			leave_this = False
			for candidate in list_of_candidates:
				if candidate in duplicate_dict[prot_id]:
					logf.write("%s\t%s\tRepresented\t%s\n" % (seq_ID, candidate, prot_id))
					leave_this = True
					break
			if leave_this:
				continue
		iden = int(tokens[9])
		if max_iden == iden:
			list_of_candidates.append(prot_id)
			outf.write("%s\t%s\n" % (line[:-1], seq_ID))
			continue
		iden_ratio = float(tokens[9]) / float(tokens[3])
		if max_iden_ratio == iden_ratio:
			list_of_candidates.append(prot_id)
			outf.write("%s\t%s\n" % (line[:-1], seq_ID))
			continue
		diff = abs(int(tokens[8]) - int(tokens[3])) + int(tokens[11])
		if min_diff == diff:
			list_of_candidates.append(prot_id)
			outf.write("%s\t%s\n" % (line[:-1], seq_ID))
			continue
		tar_range = tokens[7].split("-")
		tar_start = int(tar_range[0])
		if tar_start == 1:
			tar_end = float(tar_range[1])
			if tar_end / float(tokens[3]) >= 0.8:
				list_of_candidates.append(prot_id)
				outf.write("%s\t%s\n" % (line[:-1], seq_ID))

# create the duplicate set

duplicate_dict = {}
origin_ks = set([])
for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	if tokens[0] not in duplicate_dict:
		duplicate_dict[tokens[0]] = set([tokens[0]])
		origin_ks.add(tokens[0])
	duplicate_dict[tokens[0]].add(tokens[1])

for k in origin_ks:
	for k2 in duplicate_dict[k]:
		duplicate_dict[k2] = duplicate_dict[k]

## good through the list
orf_id = "XXX"
lines = []
outf = open(sys.argv[3], 'w')
logf = open(sys.argv[3] + ".log", 'w')

for line in open(sys.argv[2]):
	tokens = line[:-1].split("\t")
	if tokens[0] == orf_id:
		lines.append(line)
	else:
		process_lines(lines, outf, logf, duplicate_dict)
		orf_id = tokens[0]
		lines = [line]
process_lines(lines, outf, logf, duplicate_dict)

outf.close()
logf.close()
