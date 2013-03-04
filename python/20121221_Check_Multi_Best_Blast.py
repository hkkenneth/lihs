# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 27-12-2012 
## Usage: python ~/code/python/20121221_Check_Multi_Best_Blast.py <ID LIST> <BLAST RESULT WITH SYMBOL> <BLAST RESULT WITHOUT SYMBOL> <OUTPUT>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/20121221_Check_Multi_Best_Blast.py to get usage'

seq_id_dict = {}
for line in open(sys.argv[1], 'r'):
	seq_id_dict[line[:line.rfind("_")]] = set([])

name_dict = {}

iden_dict = {}

for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	name_dict[tokens[17].upper()] = tokens[2][tokens[2].find(" ") + 1 : tokens[2].rfind("[") - 1]
	if tokens[12] == "0.0":
		id = tokens[0][:tokens[0].rfind("_")]
		if id in seq_id_dict:
#			if tokens[17].upper().startswith("LOC"):
#				continue
#			if tokens[17].upper().endswith("RIK"):
#				continue
#			if tokens[17].upper().endswith("RIK1"):
#				continue
#			if tokens[17].upper().endswith("RIK2"):
#				continue
			gene_sym = tokens[17].upper()
			seq_id_dict[id].add(gene_sym)
			iden = float(tokens[9]) / float(tokens[3])
			if id in iden_dict:
				if gene_sym in iden_dict[id]:
					iden_dict[id][gene_sym] = max(iden, iden_dict[id][gene_sym])
				else:
					iden_dict[id][gene_sym] = iden
			else:
				iden_dict[id] = {}
				iden_dict[id][gene_sym] = iden
				

for line in open(sys.argv[3], 'r'):
	tokens = line.split("\t")
	if tokens[12] == "0.0":
		id = tokens[0][:tokens[0].rfind("_")]
		if id in seq_id_dict:
			seq_id_dict[id].add("THIS_IS_NOT_GENE_SYM")

outf = open(sys.argv[4], 'w')
outf4 = open(sys.argv[4] + ".new", 'w')
outf2 = open(sys.argv[4] + ".extra", 'w')
outf3 = open(sys.argv[4] + ".multi", 'w')

by_gs_dict = {}

gs1 = set([])
gs2 = set([])
for k in seq_id_dict.keys():
	if "THIS_IS_NOT_GENE_SYM" in seq_id_dict[k]:
		outf.write("%s\t%s\t-\n" % (k, "NO_GENE_SYMBOL"))
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

sorted_keys2 = seq_id_dict.keys()
sorted_keys2.sort()

for k in sorted_keys2:
	if "THIS_IS_NOT_GENE_SYM" not in seq_id_dict[k]:
		if len(seq_id_dict[k]) != 1:
			str2 = k + "\t" + str(len(seq_id_dict[k]))
			gs = list(seq_id_dict[k])
			gs.sort()
			for g in gs:
				str3 = str(iden_dict[k][g])
				str2 = str2 + "\t" + g + "(" + str3[:min(5, len(str3))] + ")"
			outf4.write("%s\n" % str2)

outf4.close()
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
