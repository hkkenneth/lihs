# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 27-12-2012 
## Usage: python ~/code/python/20121224_Check_Multi_Best_Blast_Not_0.0.py <ID LIST> <BLAST RESULT WITH SYMBOL> <BLAST RESULT WITHOUT SYMBOL> <OUTPUT> <GENE SYMBOL CONVERSION>

import sys
if len(sys.argv) < 6:
        raise SystemExit, 'use grep "##" ~/code/python/20121224_Check_Multi_Best_Blast_Not_0.0.py to get usage'

gs_convert = {}
for line in open(sys.argv[5], 'r'):
	tokens = line[:-1].split("\t")
	gs_convert[tokens[0].upper()] = tokens[1].upper()

seq_id_dict = {}
line_dict3 = {}
lines_dict2 = {}
iden_dict = {}
name_dict = {}
lines_dict1 = {}
percent_dict = {}

for line in open(sys.argv[1], 'r'):
	id = line.split("\t")[0]
	id2 = id[:id.rfind("_")]
	seq_id_dict[id2] = set([])
	line_dict3[id2] = []
	lines_dict2[id2] = []
	lines_dict1[id2] = []
	iden_dict[id2] = {}
	percent_dict[id2] = 0.0

for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	gs = tokens[17].upper()
	if gs in gs_convert:
		gs = gs_convert[gs]
	name_dict[gs] = tokens[2][tokens[2].find(" ") + 1 : tokens[2].rfind("[") - 1]
	id = tokens[0][:tokens[0].rfind("_")]
	if id in seq_id_dict:
		lines_dict1[id].append(line)
		percent_dict[id] = max(percent_dict[id], (float(tokens[9]) / float(tokens[3])))

for line in open(sys.argv[3], 'r'):
	tokens = line.split("\t")
	id = tokens[0][:tokens[0].rfind("_")]
	if id in seq_id_dict:
		lines_dict2[id].append(line)
		percent_dict[id] = max(percent_dict[id], (float(tokens[9]) / float(tokens[3])))

for id in percent_dict.keys():
	if id in lines_dict1:
		for line in lines_dict1[id]:
			tokens = line[:-1].split("\t")
			gene_sym = tokens[17].upper()
			if gene_sym in gs_convert:
				gene_sym = gs_convert[gene_sym]
			if float(tokens[9]) / float(tokens[3]) > (percent_dict[id] * 0.95):
				seq_id_dict[id].add(gene_sym)
				line_dict3[id].append(line)
			iden = float(tokens[9]) / float(tokens[3])
			if gene_sym in iden_dict[id]:
				iden_dict[id][gene_sym] = max(iden, iden_dict[id][gene_sym])
			else:
				iden_dict[id][gene_sym] = iden
	if id in lines_dict2:
		for line in lines_dict2[id]:
			tokens = line[:-1].split("\t")
			if float(tokens[9]) / float(tokens[3]) > (percent_dict[id] * 0.95):
				seq_id_dict[id].add("THIS_IS_NOT_GENE_SYM")
				line_dict3[id].append(line)


outf = open(sys.argv[4], 'w')
outf2 = open(sys.argv[4] + ".extra", 'w')
outf3 = open(sys.argv[4] + ".multi", 'w')
outf4 = open(sys.argv[4] + ".multi.new", 'w')
outf5 = open(sys.argv[4] + ".single", 'w')
outf6 = open(sys.argv[4] + ".no_gs", 'w')

by_gs_dict = {}

gs1 = set([])
gs2 = set([])
for k in seq_id_dict.keys():
	if "THIS_IS_NOT_GENE_SYM" in seq_id_dict[k]:
		outf.write("%s\t%s\t-\n" % (k, "NO_GENE_SYMBOL"))
		for line in line_dict3[k]:
			outf6.write(line)
	else:
		outf.write("%s\t%i\t%s\n" % (k, len(seq_id_dict[k]), str(seq_id_dict[k])))
		if len(seq_id_dict[k]) == 1:
			gs1 = gs1 | seq_id_dict[k]
		else:
			gs2 = gs2 | seq_id_dict[k]
		for gs in seq_id_dict[k]:
			k2 = "%s(%i)" % (k, len(seq_id_dict[k]))
			if gs in by_gs_dict:
				by_gs_dict[gs].append(k2)
			else:
				by_gs_dict[gs] = [k2]

outf6.close()

sorted_keys2 = seq_id_dict.keys()
sorted_keys2.sort()
for k in sorted_keys2:
	if "THIS_IS_NOT_GENE_SYM" not in seq_id_dict[k]:
		str2 = k + "\t" + str(len(seq_id_dict[k]))
		gs = list(seq_id_dict[k])
		gs.sort()
		for g in gs:
			str3 = str(iden_dict[k][g])
			str2 = str2 + "\t" + g + "(" + str3[:min(5, len(str3))] + ")"
		if len(seq_id_dict[k]) != 1:
			outf4.write("%s\n" % str2)
		else:
			outf5.write("%s\n" % str2)
outf4.close()		
outf5.close()

sorted_keys = by_gs_dict.keys()
sorted_keys.sort()
for gs in sorted_keys:
	str1 = gs + "\t" + name_dict[gs] + "\t" + str(len(by_gs_dict[gs]))
	by_gs_dict[gs].sort()
	for contig in by_gs_dict[gs]:
		str1 = str1 + "\t" + contig
	outf3.write("%s\n" % str1)
					
outf2.write("%i\n" % len(gs1))
outf2.write("%i\n" % len(gs2))
outf2.write("%i\n" % len(gs1 & gs2))
outf2.write("%s\n" % str(gs1 & gs2))
outf2.write("%s\n" % str(gs1))
outf2.write("%s\n" % str(gs2))
outf2.close()
outf.close()
outf3.close()
