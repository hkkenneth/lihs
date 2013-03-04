# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20130101_Contig_To_HDM_Table.py <ALL BLAST RESULT> <SELECTED> <GENE SYMBOL> <OUTPUT>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/20130101_Contig_To_HDM_Table.py to get usage'

selected = set([])
the_dict = {}
for line in open(sys.argv[2], 'r'):
	id = line[:line.rfind("_")]
	selected.add(id)
	the_dict[id] = [[],[],[]]

gs_dict = {}
for line in open(sys.argv[3], 'r'):
	tokens = line.split("\t")
	gs_dict[tokens[0]] = tokens[3].upper()

logf = open(sys.argv[4] + ".log" , 'w')
outf = open(sys.argv[4] + ".out" , 'w')
suppf = open(sys.argv[4] + ".out.supp" , 'w')

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
	str1 = contig
	for list1 in the_dict[contig]:
		if len(list1) == 0:
			str1 = str1 + "\t-\t-\t-\t-\t-"
		else:
			best_line = list1[0]
			for line in list1:
				tok = line.split("\t")
				bt = best_line.split("\t")
				if float(tok[9]) / float(tok[3]) > float(bt[9]) / float(bt[3]):
					best_line = line
			best_tokens = best_line.split("\t")
			gs = "NO_GENE_SYMBOL"
			prot_id = best_tokens[2].split(" ")[0]
			if prot_id in gs_dict:
				gs = gs_dict[prot_id]
			str1 = str1 + "\t%s\t%s\t%s\t%s\t%s" % (best_tokens[2], gs, best_tokens[3], best_tokens[8], best_tokens[9])

	outf.write("%s\n" % str1)

outf.close()
logf.close()
