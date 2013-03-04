# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 18-12-2012
## Usage: python ~/code/python/20121217_CDS_Prediction.py <INPUT> <ORF FASTA> <OUTPUT> <LEN FILE>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/20121217_CDS_Prediction.py to get usage'

rec_dict = {}
from Bio import SeqIO
for rec in SeqIO.parse(sys.argv[2], "fasta"):
	rec_dict[rec.id] = rec

outf1 = open(sys.argv[3] + ".dist", 'w')
outf2 = open(sys.argv[3] + ".size", 'w')
outf3 = open(sys.argv[3] + ".size_per_cds", 'w')
outf4 = open(sys.argv[3] + ".size_per_cds.stop", 'w')
outf5 = open(sys.argv[3] + ".size_per_cds.continue", 'w')

cds_dict = {}

#max_line_dict = {}
#max_score_dict = {}

len_dict = {}
for line in open(sys.argv[4], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

full_cds = set([])
cds_ref_len_dict = {}

for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	eff_len = float(tokens[8]) - float(tokens[11])
	prot_len = float(tokens[3])
	iden = float(tokens[9])
	if (iden / eff_len < 0.5) or (eff_len / prot_len < 0.7):
		continue
	# 1-based
	q_start = int(tokens[6].split("-")[0])
	s_start = int(tokens[7].split("-")[0])
	exp_m = q_start - s_start + 1	# still 1-based
	seq = rec_dict[tokens[0]].seq
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
	#score = iden / prot_len
	#seq_id = tokens[0][:tokens[0].rfind("_")]
	#if seq_id not in max_line_dict:
	#	max_line_dict[seq_id] = line
	#	max_score_dict[seq_id] = score
	#elif score > max_score_dict[seq_id]:
	#	max_line_dict[seq_id] = line
	#	max_score_dict[seq_id] = score
	full = True
	orf = tokens[0]
	range = orf[orf.rfind("_")+1:].split("-")
	if int(range[0]) < int(range[1]):
		if int(range[1]) + 3 > len_dict[orf[:orf.rfind("_")]]:
			full = False
	elif int(range[1]) < 4:
		full = False

	# size would be 1000000 only if there is no M in the seq...
	if cds_pos != -1:
		cds = str(seq[cds_pos:])
		if cds in cds_dict:
			cds_dict[cds] = min(cds_dict[cds], int(tokens[3]) - size)
			if abs(len(cds) - cds_ref_len_dict[cds]) > abs(len(cds) - int(tokens[3])):
				cds_ref_len_dict[cds] = int(tokens[3])				
		else:
			cds_dict[cds] = int(tokens[3]) - size
			cds_ref_len_dict[cds] = int(tokens[3])
		if full:
			full_cds.add(cds)
	outf1.write("%s\t%i\n" % (tokens[0], nearest))
	outf2.write("%s\t%i\t%i\t%i\n" % (tokens[0], int(tokens[3]) - size, int(tokens[3]), size))
outf1.close()
outf2.close()
	
#for k in max_line_dict.keys():
#	line = max_line_dict[k]
#	tokens = line[:-1].split("\t")


for k in cds_dict.keys():
	outf3.write("%i\t%i\n" % (len(k), cds_dict[k]))
	if k in full_cds:
		outf4.write("%i\t%i\n" % (cds_ref_len_dict[k], cds_dict[k]))
	else:
		outf5.write("%i\t%i\n" % (cds_ref_len_dict[k], cds_dict[k]))
outf3.close()
outf4.close()
outf5.close()
