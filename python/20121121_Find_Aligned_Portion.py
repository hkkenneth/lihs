# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121121_Find_Aligned_Portion.py <REFERENCE FASTA> <CONTIG FASTA> <LIST> <OUTPUT PREFIX>

import sys
if len(sys.argv) < ___:
        raise SystemExit, 'use grep "##" ~/code/python/_________.py to get usage'
import subprocess
from Bio import SeqIO

def cal_score(lines, logf):
	length = 0
	star = 0
	colon = 0
	dot = 0
	space = 0
	for line in lines:
		s = line[36:-1]
		length += len(s)
		star += s.count("*")
		colon += s.count(":")
		dot += s.count(".")
		space += s.count(" ")
	score = star + colon * 0.5 + dot * 0.25 - space
	logf.write("Len=%i, Star=%i, Colon=%i, Dot=%i, Space=%i, Score=%s\n" % (length, star, colon, dot, space,str(score)))
	return score


def run_alignment(counter, counter3, contig_dict, prot_rec, record_dict2, prefix_param, logf, best_dict, score_dict, short_dict):
	logf.write("--------------------------------------------\n")
	logf.write("Protein: %s\n" % prot_rec.description)
	logf.write("Length: %i\n" % len(prot_rec.seq))
	counter2 = 0
	bestScore = 0.0
	bestContig = None
	maxAvg = 0.0
	maxAvgContig = None
	for k in contig_dict.keys():
		if contig_dict[k][0] > maxAvg:
			maxAvgContig = contig_dict[k][1]
			maxAvg = contig_dict[k][0]
		counter2 += 1
		prefix = prefix_param + "." + str(counter) + "-" + str(counter2)
		f = open(prefix + ".fasta", 'w')
		SeqIO.write([prot_rec, record_dict2[contig_dict[k][1]]], f, "fasta")
		f.close()
		logf.write("%s\t%s\t" % (prefix, contig_dict[k][1]))
		subprocess.check_output(["clustalw2", "-INFILE=" + prefix + ".fasta", "-ALIGN", "-QUICKTREE", "-OUTPUT=Clustal", "-OUTFILE=" + prefix + ".clustal.output", "-STATS=clustal_stat", "-CLUSTERING=UPGMA"])
		lines = []
		for line in open(prefix + ".clustal.output", 'r'):
			lines.append(line)
		score = cal_score(lines[5::4], logf)
		first_s = lines[5][36:-1]
		short_dict[contig_dict[k][1]] = len(first_s) - len(first_s.lstrip())
		score_dict[contig_dict[k][1]] = score
		if score > bestScore:
			bestScore = score
			bestContig = contig_dict[k][1]
	logf.write("NumberOfContigs=%i\tUniqueSequences=%i\n" % (counter3, counter2))
	logf.write("BestContig: %s\tScore:%s\n" % (bestContig, str(bestScore)))
	# whether best dict has max avg
	if bestContig is not None:
		best_dict[bestContig] = (bestContig == maxAvgContig)


count_dict = {}
len_dict = {}
best_dict = {}
score_dict = {}
short_dict = {}

logf = open(sys.argv[3] + ".log", 'w')
for s in sys.argv[1:]:
	logf.write("parameters: %s\n" % s)

record_dict1 = {}
for r in SeqIO.parse(sys.argv[1], "fasta"):
	record_dict1[r.id] = r
record_dict2 = {}
for r in SeqIO.parse(sys.argv[2], "fasta"):
	record_dict2[r.id] = r

counter = 0

prot_id = None
for line in open(sys.argv[3], 'r'):
	tokens = line.split("\t")
	this_contig_id = tokens[0].split(" ")[0]
	this_prot_id = tokens[1].split(" ")[0]
	if prot_id is None:
		prot_id = this_prot_id
		contig_dict = {}
		prot_rec = record_dict1[prot_id]
		counter3 = 0
	
	if prot_id != this_prot_id:
		counter += 1
		run_alignment(counter, counter3, contig_dict, prot_rec, record_dict2, sys.argv[4], logf, best_dict, score_dict, short_dict)
		prot_id = this_prot_id
		contig_dict = {}
		prot_rec = record_dict1[prot_id]
		counter3 = 0
		
	contig_rec = record_dict2[this_contig_id]
	avg = float(tokens[7]) / float(tokens[8])
	k = str(contig_rec.seq)
	if k in contig_dict:
		if contig_dict[k][0] >= avg:
			continue
	contig_dict[k] = []
	contig_dict[k].append(avg)
	contig_dict[k].append(this_contig_id)
	counter3 += 1

# LAST
run_alignment(counter, counter3, contig_dict, prot_rec, record_dict2, sys.argv[4], logf, best_dict, score_dict, short_dict)

newf = open(sys.argv[3] + ".auto_gold", 'w')

for line in open(sys.argv[3], 'r'):
	rate = ""
	tokens = line.split("\t")
        this_contig_id = tokens[0].split(" ")[0]
	if this_contig_id in score_dict:
		protein_len = int(tokens[3])
		rate = str(score_dict[this_contig_id] / protein_len) + "\t"
	else:
		rate = "\t"
	if this_contig_id in best_dict:
		# score > 0.8?
		if short_dict[this_contig_id] > 5:
			rate = rate + "Short-" + str(short_dict[this_contig_id])
		else:
			if (abs(int(tokens[2])-int(tokens[3])) <= 10) and (score_dict[this_contig_id] / protein_len >= 0.9):
				rate = rate + "AutoGold5"
			elif (abs(int(tokens[2])-int(tokens[3])) <= 20) and (score_dict[this_contig_id] / protein_len >= 0.8):
				rate = rate + "AutoPreGold5"
		if not best_dict[this_contig_id]:
			rate = rate + "***"
	newf.write("%s\t%s\n" % (line[:-1], rate))

logf.close()
newf.close()
