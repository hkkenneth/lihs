# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/047-4_GFF_To_044_Input.py <OUTPUT PREFIX> <LEN FILE> <INPUTS ...>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/047-4_GFF_To_044_Input.py to get usage'

outf = open(sys.argv[1] + ".py047-4.out", 'w')
nof = open(sys.argv[1] + ".py047-4.no.cut.out", 'w')
shortf = open(sys.argv[1] + ".py047-4.too.short.out", 'w')

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

#for seq_id in contig_dict.keys():
for line in open(sys.argv[2], 'r'):
	tk = line[:-1].split("\t")	# tokens
	seq_id = tk[0]
	if seq_id not in contig_dict:	# no cut site, keep the entire contig..!
		nof.write("%s\t1\t%s\n" % (seq_id, tk[1]))
		continue
	sorted_list = sorted(contig_dict[seq_id], key=cal_key)
	out_list = []
	
	first_start = -1
	last_end = -1
	all_id = ""
	count = 0
	for line in sorted_list:
		tokens = line[:-1].split("\t")
		if first_start == -1:
			if int(tokens[3]) != 1:
				str1 = "%s\t%i\t%i\n" % (seq_id, 1, int(tokens[3]) - 1)
				count += int(tokens[3]) - 1
				out_list.append(str1)
			first_start = int(tokens[4]) + 1
		else:
			str1 = "%s\t%i\t%i\n" % (seq_id, first_start, int(tokens[3]) - 1)
			count += int(tokens[3]) - first_start
			out_list.append(str1)
			first_start = int(tokens[4]) + 1
	if first_start <= len_dict[seq_id]:
		str1 = "%s\t%i\t%i\n" % (seq_id, first_start, len_dict[seq_id])
		count += len_dict[seq_id] - first_start + 1
		out_list.append(str1)
	if float(count) / len_dict[seq_id] < 0.25:
		for line in out_list:
			shortf.write(line)
	else:
		for line in out_list:
			outf.write(line)

outf.close()
shortf.close()
nof.close()
