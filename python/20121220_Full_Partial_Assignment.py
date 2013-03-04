# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 20-12-2012
## Usage: python ~/code/python/20121220_Full_Partial_Assignment.py <INPUT> <ORF FASTA>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121220_Full_Partial_Assignment.py to get usage'

rec_dict = {}
from Bio import SeqIO
for rec in SeqIO.parse(sys.argv[2], "fasta"):
	rec_dict[rec.id] = rec

def add_to_dict(cds2, line, cds_d):
	cds1 = str(cds2)
	if cds1 in cds_d:
		cds_d[cds1].append(line)
	else:
		cds_d[cds1] = [line]
	
cds_dict = {} 

outf1 = open(sys.argv[1] + ".low_cov", 'w')
outf2 = open(sys.argv[1] + ".full_1", 'w')
outf2b = open(sys.argv[1] + ".full_1.supp", 'w')
outf3 = open(sys.argv[1] + ".partial_1", 'w')	# with M
outf3b = open(sys.argv[1] + ".partial_1.supp", 'w')	# with M
outf4 = open(sys.argv[1] + ".partial_2", 'w')	# without M
outf4b = open(sys.argv[1] + ".partial_2.supp", 'w')	# without M
outf5 = open(sys.argv[1] + ".full_2", 'w')
outf5b = open(sys.argv[1] + ".full_2.supp", 'w')
outf6 = open(sys.argv[1] + ".partial_3", 'w')	# nothing before alignment
outf6b = open(sys.argv[1] + ".partial_3.supp", 'w')
outf7 = open(sys.argv[1] + ".full.per_cds", 'w')
outf8 = open(sys.argv[1] + ".cds.stat", 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	eff_len = float(tokens[8]) - float(tokens[11])
	prot_len = float(tokens[3])
	iden = float(tokens[9])
	seq = rec_dict[tokens[0]].seq

	if (iden / eff_len < 0.5) or (eff_len / prot_len < 0.7):
		# low cov
		outf1.write(line)
		continue
	
	if tokens[7].startswith("1-") and tokens[14].startswith("M"):
		cds = seq[int(tokens[6].split("-")[0])-1:]
		add_to_dict(cds, line, cds_dict)
		# full 1
		outf2.write(line)
		# CDS starting pos (1-base), CDS size, protein size
		cds_size = int(tokens[1]) - int(tokens[6].split("-")[0]) + 1
		outf2b.write("%s\t%i\t%s\n" % (tokens[6].split("-")[0], cds_size, tokens[3]))
		continue
	elif tokens[6].startswith("1-"):
		# partial 3
		outf6.write(line)
		# fragment length, protein length
		outf6b.write("%s\t%s\n" % (tokens[1], tokens[3]))
		continue

	# 1-based
	q_start = int(tokens[6].split("-")[0])
	s_start = int(tokens[7].split("-")[0])
	exp_m = q_start - s_start + 1	# still 1-based
	nearest = 1000000
	size = 1000000
	cds_pos = -1
	if exp_m > 0:
		# nearest, from the front
		m1_pos = seq[:exp_m].rfind("M")
		m1_dist = exp_m - 1 - m1_pos
		m1_size = len(seq) - m1_pos
		# m1_dist is useless if >= exp_m
		m2_pos = seq[exp_m:].find("M")
		m2_dist = m2_pos + 1
		m2_size = len(seq) - (m2_pos + exp_m)
		# m2_dist is useless if <= 0
		if (m1_pos >= 0) and (nearest > m1_dist):
			nearest = min(m1_dist, nearest)
			size = m1_size
			cds_pos = m1_pos
		if (m2_pos >= 0) and (nearest > m2_dist):
			nearest = min(m2_dist, nearest)
			size = m2_size
			cds_pos = exp_m + m2_pos
	else:
		pos = seq.find("M")
		if pos >= 0:
			nearest = 1 - exp_m + pos
			size = len(seq) - pos
			cds_pos = pos
	if cds_pos == -1:
		#partial
		outf4.write(line)
		# fragment length, protein length
		outf4b.write("%s\t%s\n" % (tokens[1], tokens[3]))
	else:
		# cds_pos is 0-based
		if cds_pos + 1 < q_start:
			cds = seq[cds_pos:]
			add_to_dict(cds, line, cds_dict)
			#full
			outf5.write(line)
			# CDS starting pos (1-base), CDS size, protein size
			cds_size = int(tokens[1]) - cds_pos			
			outf5b.write("%i\t%i\t%s\n" % ((cds_pos+1), cds_size, tokens[3]))
		else:
			#partial
			outf3.write(line)
			# fragment length, protein length
			outf3b.write("%s\t%s\n" % (tokens[1], tokens[3]))

for k in cds_dict.keys():
	# assign it to the most similar size protein
	best_line = cds_dict[k][0]
	prot_set = set([])
	for line in cds_dict[k]:
		tokens = line.split("\t")
		bt = best_line.split("\t")
		if abs(len(k) - int(bt[3])) > abs(len(k) - int(tokens[3])):
			best_line = line
		prot_set.add(tokens[2])
	for prot in prot_set:
		outf8.write("%s\t%i\t%s\n" % (k, len(prot_set), prot))	
	outf7.write("%s\t%i\t%s\n" % (best_line[:-1], len(k), k))

outf1.close()
outf2.close()
outf2b.close()
outf3.close()
outf3b.close()
outf4.close()
outf4b.close()
outf5.close()
outf5b.close()
outf6.close()
outf6b.close()
outf7.close()
outf8.close()

