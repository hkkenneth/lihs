# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/047-3_Merge_GFF.py <OUTPUT PREFIX> <LEN FILE> <INPUTS ...>
## python ~/code/python/047-3_Merge_GFF.py <OUTPUT> <...>.python007.len *cut*3

import sys
if len(sys.argv) < 2:
        raise SystemExit, 'use grep "##" ~/code/python/047-3_Merge_GFF.py to get usage'

outf = open(sys.argv[1] + ".py047-3.gff3", 'w')
logf = open(sys.argv[1] + ".py047-3.log", 'w')

len_dict = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

contig_dict = {}
for s in sys.argv[3:]:
	for line in open(s, 'r'):
		tokens = line.split("\t")
		if tokens[0] not in contig_dict:
			contig_dict[tokens[0]] = []
		contig_dict[tokens[0]].append(line)

def cal_key(line):
	tokens = line.split("\t")
	return int(tokens[3]) * 1000000000 + int(tokens[4])

cut_site_count = 0
cut_site_size = 0

for seq_id in contig_dict.keys():
	sorted_list = sorted(contig_dict[seq_id], key=cal_key)
	first_start = -1
	last_end = -1
	all_id = ""
	for line in sorted_list:
		tokens = line[:-1].split("\t")
		feature_id = tokens[8].split("=")[1]
		if first_start == -1:
			first_start = int(tokens[3])
			last_end = int(tokens[4])
			all_id = all_id + feature_id + "+"
		elif int(tokens[3]) > last_end:
			outf.write("%s\t.\tMergedCutSite\t%i\t%i\t.\t+\t.\tID=%s\n" % (seq_id, first_start, min(last_end, len_dict[seq_id]), all_id[:-1]))
			cut_site_count += 1
			cut_site_size += last_end - first_start + 1
			logf.write("%i\n" % (last_end - first_start + 1))
						
			first_start = int(tokens[3])
			last_end = int(tokens[4])
			all_id = feature_id + "+"
		elif int(tokens[3]) <= last_end:
			last_end = max(last_end, int(tokens[4]))
			all_id = all_id + feature_id + "+"
	
	outf.write("%s\t.\tMergedCutSite\t%i\t%i\t.\t+\t.\tID=%s\n" % (seq_id, first_start, min(last_end, len_dict[seq_id]), all_id[:-1]))
	cut_site_count += 1
	cut_site_size += last_end - first_start + 1
	logf.write("%i\n" % (last_end - first_start + 1))
			
logf.write("Count: %i\n" % cut_site_count)
logf.write("Size: %i\n" % cut_site_size)
