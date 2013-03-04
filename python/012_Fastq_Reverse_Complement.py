# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012
## Usage: python ~/code/python/012_Fastq_Reverse_Complement.py <FASTQ FILES....>

from Bio import SeqIO
import sys

RECORD_BUFFER_SIZE = 1000000

for s in sys.argv[1:]:
	file = open(s + ".rev", 'w')
	r_list = []
	size = 0
	for r in SeqIO.parse(s, "fastq"):
		r_list.append(r.reverse_complement())
		size += 1
		if size == RECORD_BUFFER_SIZE: 
			SeqIO.write(r_list, file, "fastq")
			r_list = []
			size = 0
	if size > 0: 
		SeqIO.write(r_list, file, "fastq")
	file.close()
