# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 20-02-2013
## Usage: python ~/code/python/20130220_Trim_76bp_Fastq_SE.py <QUALITY THRESHOLD> <START BASE> <END BASE> <INPUT FASTQ> <OUTPUT FASTQ> <LOG FILE>

from Bio import SeqIO
import sys

def get_seq(r, start, end, q_cutoff):
	# 0-based, inclusive
	qual = r.letter_annotations["phred_quality"]
	for q_val in qual[start:end]:
		if q_val < q_cutoff:
			return None
	if r.seq.find("N") >= 0:
		return None
	return r[start:end]

RECORD_BUFFER_SIZE = 1000000

q_cutoff = int(sys.argv[1])
start = int(sys.argv[2])-1
end = int(sys.argv[3])
logf = open(sys.argv[6], 'w')

logf.write("Quality Threshold: %s\n" % sys.argv[1])
logf.write("Length Threshold: %s\n" % sys.argv[2])
logf.write("Input File: %s\n" % (sys.argv[4]))
logf.write("Output File: %s\n" % (sys.argv[5]))

read1s = SeqIO.parse(sys.argv[4], "fastq-illumina")
out1 = open(sys.argv[5], 'w')

count = 0
r_list1 = []
size = 0
discard_count = 0

for r1 in read1s:
	count += 1
	new_r1 = get_seq(r1, start, end, q_cutoff)
	if new_r1 is None:
		discard_count += 1
	else:
		r_list1.append(new_r1)
		size += 1
		if size == RECORD_BUFFER_SIZE: 
			SeqIO.write(r_list1, out1, "fastq")
			r_list1 = []
			size = 0
if size > 0: 
	SeqIO.write(r_list1, out1, "fastq")

logf.write("Processed Reads: %i\n" % count)
logf.write("Discarded Reads: %i\n" % discard_count)
logf.write("Output Reads: %i\n" % (count - discard_count))

out1.close()
logf.close()
