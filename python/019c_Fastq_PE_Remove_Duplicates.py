# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 25-11-2012
## Usage: python ~/code/python/019c_Fastq_PE_Remove_Duplicates.py <FILE LIST 1> <FILENAME POSTFIX> <LOG FILE>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/019c_Fastq_PE_Remove_Duplicates.py to get usage'
import os

def linesToFile(lines, f):
	for line in lines:
		f.write(line)

reads_set = set([])
postfix = sys.argv[2]
logf = open(sys.argv[3], 'w')

total_count = 0
total_dup_count = 0
file_count = 0
for line in open(sys.argv[1], 'r'):
	file_count += 1
	file_names = line[:-1].split("\t")
	f1in = open(file_names[0], 'r')
	f2in = open(file_names[1], 'r')
	f1prefix = file_names[0]	#[:file_names[0].rfind(postfix)]
	f2prefix = file_names[1]	#[:file_names[1].rfind(postfix)]
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
		fragment = f1lines[i][:-1] + f2lines[i][:-1]
		if fragment in reads_set:
			dupcount += 1
			linesToFile(f1lines[(i-1):(i+3)], f1out_d)
			linesToFile(f2lines[(i-1):(i+3)], f2out_d)
		else:
			reads_set.add(fragment)
			linesToFile(f1lines[(i-1):(i+3)], f1out_u)
			linesToFile(f2lines[(i-1):(i+3)], f2out_u)
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
	total_count += seqcount
	total_dup_count += dupcount

logf.write("Finished processing %i files: total read pairs: %i unique read pairs: %i duplicate: %i\n" % (file_count, total_count, (total_count - total_dup_count), total_dup_count))
logf.close()
