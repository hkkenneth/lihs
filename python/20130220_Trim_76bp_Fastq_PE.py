# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 20-02-2013
## Usage: python ~/code/python/20130220_Trim_76bp_Fastq_PE.py <QUALITY THRESHOLD> <START BASE> <END BASE> <INPUT FASTQ 1> <INPUT FASTQ 2> <OUTPUT FASTQ 1> <OUTPUT FASTQ 2> <LOG FILE>

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
logf = open(sys.argv[8], 'w')

logf.write("Quality Threshold: %s\n" % sys.argv[1])
logf.write("Length Threshold: %s\n" % sys.argv[2])
logf.write("Input Files: %s, %s\n" % (sys.argv[4], sys.argv[5]))
logf.write("Output Files: %s, %s\n" % (sys.argv[6], sys.argv[7]))

read1s = SeqIO.parse(sys.argv[4], "fastq-illumina")
read2s = SeqIO.parse(sys.argv[5], "fastq-illumina")
out1 = open(sys.argv[6], 'w')
out2 = open(sys.argv[7], 'w')

count = 0
r_list1 = []
r_list2 = []
size = 0
discard_count = 0

for r1 in read1s:
	r2 = read2s.next()
	count += 1
	new_r1 = get_seq(r1, start, end, q_cutoff)
	new_r2 = get_seq(r2, start, end, q_cutoff)
	if (new_r1 is None) or (new_r2 is None):
		discard_count += 1
	else:
		r_list1.append(new_r1)
		r_list2.append(new_r2)
		size += 1
		if size == RECORD_BUFFER_SIZE: 
			SeqIO.write(r_list1, out1, "fastq")
			SeqIO.write(r_list2, out2, "fastq")
			r_list1 = []
			r_list2 = []
			size = 0
if size > 0: 
	SeqIO.write(r_list1, out1, "fastq")
	SeqIO.write(r_list2, out2, "fastq")

logf.write("Processed Reads: %i\n" % count)
logf.write("Discarded Reads: %i\n" % discard_count)
logf.write("Output Reads: %i\n" % (count - discard_count))

out1.close()
out2.close()
logf.close()
