# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 09-01-2013
## Usage: python ~/code/python/019e_Fastq_PE_Remove_Duplicates_With_Stat.py <FILE LIST 1> <FILENAME POSTFIX> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/019e_Fastq_PE_Remove_Duplicates_With_Stat.py to get usage'
import os

def linesToFile(lines, f):
	for line in lines:
		f.write(line)

reads_dict = {}
postfix = sys.argv[2]
logf = open(sys.argv[3] + ".log", 'w')
statf = open(sys.argv[3] + ".stat", 'w')
overf1 = open(sys.argv[3] + ".over_rep.r1.fq", 'w')
overf2 = open(sys.argv[3] + ".over_rep.r2.fq", 'w')

over_dict = {}
cutoff = 2000

total_count = 0
total_dup_count = 0
file_count = 0
for line in open(sys.argv[1], 'r'):
	file_count += 1
	statf2 = open(sys.argv[3] + ".stat.detail." + str(file_count), 'w')
	file_names = line[:-1].split("\t")
	f1in = open(file_names[0], 'r')
	f2in = open(file_names[1], 'r')
	f1prefix = file_names[0][:file_names[0].rfind(postfix)]
	f2prefix = file_names[1][:file_names[1].rfind(postfix)]
	f1out_d = open(f1prefix + ".duplicates" + postfix, 'w')
	f2out_d = open(f2prefix + ".duplicates" + postfix, 'w')
	f1out_u = open(f1prefix + ".unique" + postfix, 'w')
	f2out_u = open(f2prefix + ".unique" + postfix, 'w')
	f1lines = f1in.readlines()
	f2lines = f2in.readlines()
	i = 1
	if f1lines[0].split(" ")[0] != f2lines[0].split(" ")[0]:
		logf.write("%s and %s do not match\n" % (file_names[0], file_names[1]))
		continue
	seqcount = 0
	dupcount = 0
	while i < len(f1lines):
		fragment = f1lines[i][10:50] + f2lines[i][10:50]
		if fragment in reads_dict:
			dupcount += 1
			reads_dict[fragment] += 1
			linesToFile(f1lines[(i-1):(i+3)], f1out_d)
			linesToFile(f2lines[(i-1):(i+3)], f2out_d)
			if reads_dict[fragment] >= cutoff:
				over_dict[fragment] = [f1lines[(i-1):(i+3)], f2lines[(i-1):(i+3)]]
		else:
			reads_dict[fragment] = 1
			linesToFile(f1lines[(i-1):(i+3)], f1out_u)
			linesToFile(f2lines[(i-1):(i+3)], f2out_u)
		statf2.write("%s\t%i\n" % (f1lines[i-1][:-1], reads_dict[fragment]))
		i += 4
		seqcount += 1
	logf.write("Finished processing %s and %s: total read pairs: %i unique read pairs: %i duplicate: %i\n" % (file_names[0], file_names[1], seqcount, (seqcount - dupcount), dupcount))
	logf.flush()
	os.fsync(logf.fileno())

	f1in.close()
	f2in.close()
	f1out_d.close()
	f2out_d.close()
	f1out_u.close()
	f2out_u.close()
	statf2.close()
	total_count += seqcount
	total_dup_count += dupcount

over_dict_2 = {}

for k in reads_dict.keys():
	statf.write("%s\t%i\n" % (k, reads_dict[k]))
	if reads_dict[k] >= cutoff:
		over_dict_2[k] = reads_dict[k]
import operator
sorted_dict = sorted(over_dict_2.iteritems(), key=operator.itemgetter(1), reverse=True)
for pair in sorted_dict:
	linesToFile(over_dict[pair[0]][0], overf1)
	linesToFile(over_dict[pair[0]][1], overf2)
	
overf1.close()
overf2.close()

statf.close()
logf.write("Finished processing %i files: total read pairs: %i unique read pairs: %i duplicate: %i\n" % (file_count, total_count, (total_count - total_dup_count), total_dup_count))
logf.close()
