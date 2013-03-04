# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 25-11-2012
## Usage: python ~/code/python/019b_Fastq_PE_Remove_Duplicates.py <FILE LIST 1> <FILE LIST 2> <FILENAME POSTFIX> <LOG FILE>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/019_Fastq_PE_Remove_Duplicates.py to get usage'
from Bio import SeqIO
import os

RECORD_BUFFER_SIZE = 1000000

reads_set = set([])
postfix = sys.argv[3]
logf = open(sys.argv[4], 'w')

for line in open(sys.argv[1], 'r'):
	file_names = line[:-1].split("\t")
	f1in = open(file_names[0], 'r')
	f2in = open(file_names[1], 'r')
	f1lines = f1in.readlines()
	f2lines = f2in.readlines()
	i = 1
	if f1lines[0].split("/")[0] != f2lines[0].split("/")[0]:
		logf.write("%s and %s do not match\n" % (file_names[0], file_names[1]))
		continue
	seqcount = 0
	while i < len(f1lines):
		reads_set.add(f1lines[i][:-1] + f2lines[i][:-1])
		i += 4
		seqcount += 1
	logf.write("Finished reading %s and %s: total read pairs: %i\n" % (file_names[0], file_names[1], seqcount))
	logf.flush()
	os.fsync(logf.fileno())

total_count = 0
total_dup_count = 0
file_count = 0
for line in open(sys.argv[2], 'r'):
	file_count += 1
	file_names = line[:-1].split("\t")
	f1in = open(file_names[0], 'r')
	f2in = open(file_names[1], 'r')
	read1s = SeqIO.parse(file_names[0], "fastq")
	read2s = SeqIO.parse(file_names[1], "fastq")
	f1prefix = file_names[0][:file_names[0].rfind(postfix)]
	f2prefix = file_names[1][:file_names[1].rfind(postfix)]
	f1out_d = open(f1prefix + ".duplicates" + postfix, 'w')
	f2out_d = open(f2prefix + ".duplicates" + postfix, 'w')
	f1out_u = open(f1prefix + ".unique" + postfix, 'w')
	f2out_u = open(f2prefix + ".unique" + postfix, 'w')
	first_line = True
	r_list_1 = []
	r_list_2 = []
	r_list_3 = []
	r_list_4 = []
	size_1 = 0
	size_2 = 0
	dupcount = 0
	seqcount = 0
	for r1 in read1s:
		r2 = read2s.next()
		seqcount += 1
		if first_line:
			first_line = False
			if r1.id.split("/")[0] != r2.id.split("/")[0]:
				logf.write("%s and %s do not match\n" % (file_names[0], file_names[1]))
				continue
		fragment = str(r1.seq) + str(r2.seq)
		if fragment in reads_set:
			dupcount += 1
			size_2 += 1
			r_list_3.append(r1)
			r_list_4.append(r2)
		else:
			reads_set.add(fragment)
			size_1 += 1
			r_list_1.append(r1)
			r_list_2.append(r2)
		if size_1 == RECORD_BUFFER_SIZE:
			SeqIO.write(r_list_1, f1out_u, "fastq")
			SeqIO.write(r_list_2, f2out_u, "fastq")
			r_list_1 = []
			r_list_2 = []
			size_1 = 0
		if size_2 == RECORD_BUFFER_SIZE:
			SeqIO.write(r_list_3, f1out_d, "fastq")
			SeqIO.write(r_list_4, f2out_d, "fastq")
			r_list_3 = []
			r_list_4 = []
			size_2 = 0
	if size_1 > 0:
		SeqIO.write(r_list_1, f1out_u, "fastq")
		SeqIO.write(r_list_2, f2out_u, "fastq")
	if size_2 > 0:
		SeqIO.write(r_list_3, f1out_d, "fastq")
		SeqIO.write(r_list_4, f2out_d, "fastq")
	f1out_d.close()
	f2out_d.close()
	f1out_u.close()
	f2out_u.close()
	logf.write("Finished processing %s and %s: total read pairs: %i unique read pairs: %i duplicate: %i\n" % (file_names[0], file_names[1], seqcount, (seqcount - dupcount), dupcount))
	total_count += seqcount
	total_dup_count += dupcount

logf.write("Finished processing %i files: total read pairs: %i unique read pairs: %i duplicate: %i\n" % (file_count, total_count, (total_count - total_dup_count), total_dup_count))
logf.close()
