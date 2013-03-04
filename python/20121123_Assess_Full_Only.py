# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/_______.py <_________>
## python ~/code/python/20121123_Assess_Same_E_rate.py dog human mouse

import sys

contig_dict = {}

for s in sys.argv[1:]:
	for line in open(s, 'r'):
		tokens = line[:-1].split("\t")
		id = tokens[17]
		if id in contig_dict:
			contig_dict[id].append(line[:-1])
		else:
			contig_dict[id] = [line[:-1]]

count = 0
count_dict = {0:0, 1:0, 2:0, 3:0}
for k in contig_dict.keys():
	count += 1
	same_count = 0
	for l in contig_dict[k]:
		tokens = l[:-1].split("\t")
		s_range = tokens[7].split("-")
		s_start = int(s_range[0])
		s_end = float(s_range[1])
		hit_len = float(tokens[3])
		if (s_start == 1) and (s_end / hit_len > 0.9):
			same_count += 1
	count_dict[same_count] += 1

print count
print count_dict
