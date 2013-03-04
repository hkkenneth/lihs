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
	min_e = 1000.0
	count += 1
	for l in contig_dict[k]:
		min_e = min(min_e, float(l.split("\t")[5]))
	same_count = 0
	for l in contig_dict[k]:
		if float(l.split("\t")[5]) == min_e:
			same_count += 1
	count_dict[same_count] += 1

print count
print count_dict
