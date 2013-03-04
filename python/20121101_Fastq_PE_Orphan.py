# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012
## Usage: python ~/code/python/20121101_Fastq_PE_Orphan.py <EXCLUDE FASTQ 1> <EXCLUDE FASTQ 2> <INPUT FASTQ 1> <INPUT FASTQ 2> <OUTPUT FASTQ 1> <OUTPUT FASTQ 2>

from Bio import SeqIO
import sys

RECORD_BUFFER_SIZE = 100000

exclude_set = set([])

for s in sys.argv[1:3]:
	for r in SeqIO.parse(s, "fastq"):
		print r.id[:-2]
		exclude_set.add(r.id[:-2])

read1s = SeqIO.parse(sys.argv[3], "fastq")
read2s = SeqIO.parse(sys.argv[4], "fastq")
out1 = open(sys.argv[5], 'w')
out2 = open(sys.argv[6], 'w')

r_list1 = []
r_list2 = []
size = 0

for r1 in read1s:
	r2 = read2s.next()
	if r1.id[:-2] not in exclude_set:
		r_list1.append(r1)
		r_list2.append(r2)
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

out1.close()
out2.close()
