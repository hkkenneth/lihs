# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 19-01-2013
## Usage: python ~/code/python/036_Py010_Selection.py <INPUT> <OUTPUT> <ORF FASTA> <GENE SYMBOL>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/036_Py010_Selection.py to get usage'

from Bio import SeqIO
record_dict = {}
for record in SeqIO.parse(sys.argv[3], "fasta"):
	record_dict[record.id] = record

gs_dict = {}
for line in open(sys.argv[4], 'r'):
	tokens = line.split("\t")
	gs_dict[tokens[0]] = tokens[3].upper()

tokens_dict = {}
line_dict = {}
seq_count_dict = {}
id_dict = {}
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	line_dict[tokens[16]] = line
	tokens_dict[tokens[16]] = tokens
	id = tokens[0][:tokens[0].rfind("_")]
	id_dict[tokens[0]] = id
	if id in seq_count_dict:
		seq_count_dict[id] += 1
	else:
		seq_count_dict[id] = 1

count_str_dict = {}
for k in tokens_dict.keys():
	orf_id = tokens_dict[k][0]
	if seq_count_dict[id_dict[orf_id]] == 1:
		count_str_dict[k] = "SINGLE\t1"
	else:
		count_str_dict[k] = "MULTI\t%i" % seq_count_dict[id_dict[orf_id]]

cov_dict = {}
cov_start_dict = {}
cov_end_dict = {}
iden_dict = {}
contain_stop_dict = {}
assigned_gs_dict = {}
for k in tokens_dict.keys():
	tokens = tokens_dict[k]
	ref_len = float(tokens[3])
	align_len = float(tokens[8]) - float(tokens[11])
	iden_len = float(tokens[9])
	if align_len / ref_len > 0.9:
		cov_dict[k] = "HIGH_COV\t%s" % str(align_len / ref_len)
	elif align_len / ref_len > 0.7:
		cov_dict[k] = "MED_COV\t%s" % str(align_len / ref_len)
	else:
		cov_dict[k] = "LOW_COV\t%s" % str(align_len / ref_len)
	if iden_len / align_len > 0.9:
		iden_dict[k] = "HIGH_IDEN\t%s" % str(iden_len / align_len)
	elif iden_len / align_len > 0.7:
		iden_dict[k] = "MED_IDEN\t%s" % str(iden_len / align_len)
	else:
		iden_dict[k] = "LOW_IDEN\t%s" % str(iden_len / align_len)
	if (tokens[7].startswith("1-")) and (tokens[14][0]=="M"):
		cov_start_dict[k] = "COV_START_YES"
	else:
		cov_start_dict[k] = "COV_START_NO"
	if "*" in tokens[13]:
		contain_stop_dict[k] = "CONTAIN_STOP_YES"
	else:
		contain_stop_dict[k] = "CONTAIN_STOP_NO"
	rec = record_dict[tokens[0]]
	start_pos = int(tokens[6].split("-")[0]) - 1
	if "*" in rec[start_pos:]:
		cov_end_dict[k] = "COV_END_YES"
	else:
		cov_end_dict[k] = "COV_END_NO"
	prot_id = tokens[2].split(" ")[0]
	if prot_id in gs_dict:
		assigned_gs_dict[k] = gs_dict[prot_id]	
	else:
		assigned_gs_dict[k] = "CANNOT_ASSIGNE_GENE_SYMBOL"
		
ks = tokens_dict.keys()
ks.sort()
outf = open(sys.argv[2], 'w')
for k in ks:
	outf.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (line_dict[k][:-1], count_str_dict[k], cov_dict[k], cov_start_dict[k], iden_dict[k], contain_stop_dict[k], cov_end_dict[k], assigned_gs_dict[k]))

outf.close()
