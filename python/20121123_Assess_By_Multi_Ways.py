# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/_______.py <_________>

import sys

contig_dict = {}
skip_contig_set = set([])

for line in open(sys.argv[1], 'r'):
	skip_contig_set.add(line[:-1])

for s in sys.argv[2:]:
	for line in open(s, 'r'):
		tokens = line[:-1].split("\t")
		id = tokens[17]
		if id in contig_dict:
			contig_dict[id].append(line)
		else:
			contig_dict[id] = [line]

count = 0
count2 = 0
count3 = 0
count_dict = {0:0, 1:0, 2:0, 3:0}
count_dict2 = {0:0, 1:0, 2:0, 3:0}
count_dict3 = {0:0, 1:0, 2:0, 3:0}
outf = open("FINAL_ASSIGNMENT", 'w')
skip_count = 0
for k in contig_dict.keys():
	if k in skip_contig_set:
		skip_count += 1
		continue
	count += 1
	same_count = 0
	full_lines = []
	for l in contig_dict[k]:
		tokens = l[:-1].split("\t")
		s_range = tokens[7].split("-")
		s_start = float(s_range[0])
		s_end = float(s_range[1])
		hit_len = float(tokens[3])
		#if (s_start == 1) and (s_end / hit_len > 0.9):
		if ((s_end - s_start + 1) / hit_len > 0.9):
			same_count += 1
			full_lines.append(l)
	count_dict[same_count] += 1
	if same_count == 1:
		outf.write(full_lines[0])
	if same_count <= 1:
		continue
	count2 += 1
	same_count = 0
	max_iden = 0
	max_iden_lines = []
	for l in full_lines:
		tokens = l.split("\t")
		iden_posi_gap = int(tokens[9]) + int(tokens[10]) - int(tokens[11])
		max_iden = max(max_iden, iden_posi_gap)
	for l in full_lines:
		tokens = l.split("\t")
		iden_posi_gap = int(tokens[9]) + int(tokens[10]) - int(tokens[11])
		if iden_posi_gap == max_iden:
			same_count += 1
			max_iden_lines.append(l)
	count_dict2[same_count] += 1
	if same_count == 1:
		outf.write(max_iden_lines[0])
	if same_count <= 1:
		continue

	count3 += 1
	same_count = 0
	min_e = 10000.0	
	min_e_lines = []
	for l in max_iden_lines:
		min_e = min(min_e, float(l.split("\t")[5]))
	for l in max_iden_lines:
       	        if float(l.split("\t")[5]) == min_e:
               	        same_count += 1
			min_e_lines.append(l)
        count_dict3[same_count] += 1
	outf.write(min_e_lines[0])
outf.close()
print "Skipped:"
print skip_count
print "By 90% Coverage:"
print count
print count_dict
print "By Max Iden+Posi-Gaps:"
print count2
print count_dict2
print "By Min E:"
print count3
print count_dict3
