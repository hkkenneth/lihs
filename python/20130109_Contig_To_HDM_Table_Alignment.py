# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 09-01-2013 
## Usage: python ~/code/python/20130109_Contig_To_HDM_Table_Alignment.py <ALL BLAST RESULT> <SELECTED> <GENE SYMBOL> <OUTPUT>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/20130109_Contig_To_HDM_Table_Alignment.py to get usage'

selected = set([])
the_dict = {}
for line in open(sys.argv[2], 'r'):
	id = line[:-1]
	selected.add(id)
	the_dict[id] = [[],[],[]]

gs_dict = {}
for line in open(sys.argv[3], 'r'):
	tokens = line.split("\t")
	gs_dict[tokens[0]] = tokens[3].upper()

logf = open(sys.argv[4] + ".log" , 'w')
outf = open(sys.argv[4] + ".out" , 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	id = tokens[0][:tokens[0].rfind("_")]
	if id in selected:
		species = tokens[2][tokens[2].rfind("[")+1:]
		if species.startswith("Homo"):
			the_dict[id][0].append(line)
		elif species.startswith("Canis"):
			the_dict[id][1].append(line)
		elif species.startswith("Mus"):
			the_dict[id][2].append(line)
		else:
			logf.write(line)

contigs = the_dict.keys()
contigs.sort()
for contig in contigs:
	best_90_percent_lists = []
	for list1 in the_dict[contig]:
		list2 = []
		if len(list1) > 0:
			best_line = list1[0]
			for line in list1:
				tok = line.split("\t")
				bt = best_line.split("\t")
				if float(tok[9]) / float(tok[3]) > float(bt[9]) / float(bt[3]):
					best_line = line
			for line in list1:
				tok = line.split("\t")
				bt = best_line.split("\t")
				if float(tok[9]) / float(tok[3]) > float(bt[9]) / float(bt[3]) * 0.90:
					list2.append(line)
		best_90_percent_lists.append(list2)
	num_row = 0
	for list2 in best_90_percent_lists:
		num_row = max(num_row, len(list2))
	for i in range(num_row):
		str1 = contig
		str2 = contig
		str3 = contig
		for list2 in best_90_percent_lists:
			if len(list2)-1 < i:
				str1 = str1 + "\t-\t-\t-\t-\t-\t-\t-\t-"
				str2 = str2 + "\t-\t-\t-\t-\t-\t-\t-\t-"
				str3 = str3 + "\t-\t-\t-\t-\t-\t-\t-\t-"
			else:
				best_tokens = list2[i].split("\t")
				gs = "NO_GENE_SYMBOL"
				prot_id = best_tokens[2].split(" ")[0]
				if prot_id in gs_dict:
					gs = gs_dict[prot_id]
				str1 = str1 + "\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (best_tokens[2], gs, best_tokens[3], best_tokens[8], best_tokens[9], best_tokens[10], best_tokens[11], best_tokens[13])
				str2 = str2 + "\t-\t-\t-\t-\t-\t-\tMatch Line\t%s" % best_tokens[14]
				str3 = str3 + "\t-\t-\t-\t-\t-\t-\tRef Line\t%s" % best_tokens[15]

		outf.write("%s\n%s\n%s\n" % (str1, str2, str3))

outf.close()
logf.close()
