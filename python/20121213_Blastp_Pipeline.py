# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 13-12-2012
## Usage: python ~/code/python/20121213_Blastp_Pipeline.py <LEN FILE> <ORF FASTA> <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121213_Blastp_Pipeline.py to get usage'

def orf_stat(orf_count, orf_sum, l):
	if len(orf_set) in orf_count:
		orf_count[len(orf_set)] += 1
	else:
		orf_count[len(orf_set)] = 1
	if len(orf_set) in orf_sum:
		orf_sum[len(orf_set)] += l
	else:
		orf_sum[len(orf_set)] = l

def get_best_line(lines):
	best_line = ""
	best_score = 0
	
	for line in lines:
		tokens = line.split("\t")
		score = int(tokens[9]) + int(tokens[10]) - int(tokens[11])*2
		if score > best_score:
			best_score = score
			best_line = line
	return best_line

len_dict = {}
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

rec_dict = {}
from Bio import SeqIO
for rec in SeqIO.parse(sys.argv[2], "fasta"):
	rec_dict[rec.id] = rec

line_dict = {}
for line in open(sys.argv[3], 'r'):
	id = line[:line[:line.find("\t")].rfind("_")]
	if id in line_dict:
		line_dict[id].add(line)
	else:
		line_dict[id] = set([line])

outf1 = open(sys.argv[4] + ".orf_count", 'w')
outf2 = open(sys.argv[4] + ".seq_stat", 'w')
outf3 = open(sys.argv[4] + ".max_match", 'w')
outf4 = open(sys.argv[4] + ".5.best", 'w')
outf5 = open(sys.argv[4] + ".4.not_cov_end", 'w')
outf6 = open(sys.argv[4] + ".4.not_full", 'w')
outf7 = open(sys.argv[4] + ".4.not_start_m", 'w')
outf8 = open(sys.argv[4] + ".4.not_high_cov", 'w')
outf9 = open(sys.argv[4] + ".4.not_high_iden", 'w')
logf = open(sys.argv[4] + ".log", 'w')

orf_count = {}
orf_sum = {}

for id in line_dict.keys():
	orf_set = set([])
	for line in line_dict[id]:
		tokens = line.split("\t")
		if float(tokens[9]) / float(tokens[8]) > 0.5:
			orf_set.add(tokens[0])
#	if len(orf_set) == 0:	
	outf1.write("%s\t%i\t%i\n" % (id, len_dict[id], len(orf_set)))
	orf_stat(orf_count, orf_sum, len_dict[id])
	if len(orf_set) != 1:
		continue
	full = True
	for orf in orf_set:
		range = orf[orf.rfind("_")+1:].split("-")
		if int(range[0]) < int(range[1]):
			if int(range[1]) + 3 > len_dict[orf[:orf.rfind("_")]]:
				full = False
		elif int(range[1]) < 4:
			full = False
	max_true_count = 0
	true_line_dict = {}
	true_dict = {}
	for line in line_dict[id]:
		high_cov = False
		high_iden = False
		start_m = False
		cov_end = False
		if full:
			true_count = 1
		else:
			true_count = 0
		tokens = line.split("\t")
		if tokens[0] not in orf_set:
			 continue
		eff_len = int(tokens[8]) - int(tokens[11])
		if eff_len / float(tokens[3]) > 0.9:
			high_cov = True
			true_count += 1
		if (float(tokens[9]) / float(tokens[8]) > 0.5) and (float(tokens[10]) / float(tokens[8]) > 0.7):
			high_iden = True
			true_count += 1
		if tokens[7].startswith("1-") and tokens[14].startswith("M"):
			start_m = True
			true_count += 1
		else:
			q_start = int(tokens[6].split("-")[0])
			s_start = int(tokens[7].split("-")[0])
			exp_m = q_start - s_start + 1
			exp_m_start = max(0, exp_m - 15)
			exp_m_end = min(int(tokens[1]), exp_m + 16)
			if (exp_m_end > 0) and (rec_dict[tokens[0]].seq[exp_m_start:exp_m_end].find("M") >= 0):
				start_m = True
				true_count += 1
			
		if abs(int(tokens[7].split("-")[1]) - int(tokens[3])) <= 15:
			cov_end = True
			true_count += 1
		line2 = "%s\t%s\t%s\t%s\t%s\t%s\n" % (line[:-1], full, high_cov, high_iden, start_m, cov_end)
		bools = [full, high_cov, high_iden, start_m, cov_end]
		if true_count in true_line_dict:
			true_line_dict[true_count].append(line2)
			true_dict[true_count].append(bools)
		else:
			true_line_dict[true_count] = [line2]
			true_dict[true_count] = [bools]
		max_true_count = max(max_true_count, true_count)
	outf2.write("%s\t%i\n" % (id, max_true_count))
	
	if max_true_count == 5:
		outf4.write(get_best_line(true_line_dict[max_true_count]))
	elif max_true_count == 4:
		not_full = []
		not_start_m = []
		not_cov_end = []
		not_high_cov = []
		not_high_iden = []
		j = 0
		for line in true_line_dict[max_true_count]:
			tokens = line.split("\t")
			true_val = true_dict[max_true_count][j]
			j += 1
			if not true_val[4]:
				not_cov_end.append(line)
			elif not true_val[0]:
				not_full.append(line)
			elif not true_val[3]:
				not_start_m.append(line)
			elif not true_val[1]:
				not_high_cov.append(line)
			elif not true_val[2]:
				not_high_iden.append(line)
		if len(not_cov_end) != 0:
			outf5.write(get_best_line(not_cov_end))
		elif len(not_full) != 0:
			outf6.write(get_best_line(not_full))
		elif len(not_start_m) != 0:
			outf7.write(get_best_line(not_start_m))
		elif len(not_high_cov) != 0:
			outf8.write(get_best_line(not_high_cov))
		elif len(not_high_iden) != 0:
			outf9.write(get_best_line(not_high_iden))
		
	for line in true_line_dict[max_true_count]:
		outf3.write("%s\t%i\n" % (line[:-1], max_true_count))

#TODO : MAX = 4, WHAT CASES ARE THERE?
#TODO RESOLVE TO UNIQUE SEQ? BY WHAT? CDS?
#WHAT ARE NEW AND WHAT ARE OLD
	
outf1.close()
outf2.close()
outf3.close()
outf4.close()
outf5.close()
outf6.close()
outf7.close()
outf8.close()
outf9.close()

for count in orf_sum.keys():
	logf.write("%i\t%s\n" % (count ,str(orf_sum[count]/float(orf_count[count]))))

logf.write("%s\n" % str(orf_count))

logf.close()
