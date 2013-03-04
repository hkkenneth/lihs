# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 04-01-2013
## Usage: python ~/code/python/019D_Fastq_SE_Remove_Duplicates.py <FILE LIST> <FILENAME POSTFIX> <LOG FILE>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/019D_Fastq_SE_Remove_Duplicates.py to get usage'
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
	file_name = line[:-1]
	f1in = open(file_name, 'r')
	f1prefix = file_name[:file_name.rfind(postfix)]
	f1out_d = open(f1prefix + ".duplicates" + postfix, 'w')
	f1out_u = open(f1prefix + ".unique" + postfix, 'w')
	f1lines = f1in.readlines()
	i = 1
	seqcount = 0
	dupcount = 0
	while i < len(f1lines):
		fragment = f1lines[i][10:40]
		if fragment in reads_set:
			dupcount += 1
			linesToFile(f1lines[(i-1):(i+3)], f1out_d)
		else:
			reads_set.add(fragment)
			linesToFile(f1lines[(i-1):(i+3)], f1out_u)
		i += 4
		seqcount += 1
	logf.write("Finished processing %s: total reads: %i unique reads: %i duplicate: %i\n" % (file_name, seqcount, (seqcount - dupcount), dupcount))
	logf.flush()
	os.fsync(logf.fileno())

	f1in.close()
	f1out_d.close()
	f1out_u.close()
	total_count += seqcount
	total_dup_count += dupcount

logf.write("Finished processing %i files: total reads: %i unique reads: %i duplicate: %i\n" % (file_count, total_count, (total_count - total_dup_count), total_dup_count))
logf.close()
