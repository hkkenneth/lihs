# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 07-01-2013
## Usage: python ~/code/python/011_Fastq_Trim_To_Longest_Part_Above_Quality_Threshold.py <QUALITY THRESHOLD> <MIN OUTPUT LEN> <OUTPUT STAT> <INPUT FASTQ 1> <INPUT FASTQ 2> <OUTPUT FASTQ 1> <OUTPUT FASTQ 2>
## if the resulting read length is <= <MIN OUTPUT LEN> then the read is discarded.

from Bio import SeqIO
import sys

def get_seq(r, q_cutoff):
	# 0-based, inclusive
	best_start = 0
	best_end = -1
	curr_start = 0
	curr_end = -1
	qual = r.letter_annotations["phred_quality"]
	for index in xrange(len(r.seq)):
		if qual[index] < q_cutoff:
			if (curr_end - curr_start) > (best_end - best_start):
				best_end = curr_end
				best_start = curr_start
			#if (len(r.seq) - ___) <= (best_end - best_start):
			#	break
			curr_start = index + 1
		else:
			curr_end = index
	if (curr_end - curr_start) > (best_end - best_start):
		best_end = curr_end
		best_start = curr_start
	if best_end - best_start >= 0:
		return r[best_start:(best_end+1)]
	return None # i.e. empty read?

def add_to_dict(val, the_dict):
	if val in the_dict:
		the_dict[val] += 1
	else:
		the_dict[val] = 1

RECORD_BUFFER_SIZE = 1000000

q_cutoff = int(sys.argv[1])
len_cutoff = int(sys.argv[2])
logf = open(sys.argv[3], 'w')

logf.write("Quality Threshold: %s\n" % sys.argv[1])
logf.write("Length Threshold: %s\n" % sys.argv[2])
logf.write("Input Files: %s, %s\n" % (sys.argv[4], sys.argv[5]))
logf.write("Output Files: %s, %s\n" % (sys.argv[6], sys.argv[7]))

pe_dict = {}
se_dict = {}

read1s = SeqIO.parse(sys.argv[4], "fastq")
read2s = SeqIO.parse(sys.argv[5], "fastq")
out1 = open(sys.argv[6], 'w')
out2 = open(sys.argv[7], 'w')

count = 0
r_list1 = []
r_list2 = []
size = 0
discard_count = 0
discard_stat_1 = {}
discard_stat_2 = {}

for r1 in read1s:
	r2 = read2s.next()
	count += 1
	new_r1 = get_seq(r1, q_cutoff)
	new_r2 = get_seq(r2, q_cutoff)
	if (new_r1 is None) or (new_r2 is None) or (len(new_r1.seq) <= len_cutoff) or (len(new_r2.seq) <= len_cutoff):
		if (new_r1 is not None) and (len(new_r1.seq) > len_cutoff):
			add_to_dict(len(new_r1.seq), discard_stat_1)
		if (new_r2 is not None) and (len(new_r2.seq) > len_cutoff):
			add_to_dict(len(new_r2.seq), discard_stat_2)
		discard_count += 1
	else:
		add_to_dict(min(len(new_r1), len(new_r2)), pe_dict)
		add_to_dict(len(new_r1), se_dict)
		add_to_dict(len(new_r2), se_dict)
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

logf.write("PE reads stat:\n%s\n\n" % str(pe_dict))
logf.write("SE reads stat:\n%s\n\n" % str(se_dict))
logf.write("Discarded reads 1 stat:\n%s\n\n" % str(discard_stat_1))
logf.write("Discarded reads 2 stat:\n%s\n\n" % str(discard_stat_2))

logf.write("Processed Reads: %i\n" % count)
logf.write("Discarded Reads: %i\n" % discard_count)
logf.write("Output Reads: %i\n" % (count - discard_count))

out1.close()
out2.close()
logf.close()
