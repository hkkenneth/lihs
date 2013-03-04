# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 22-11-2012
## Usage: python ~/code/python/016_Fastq_To_Fasta.py <FASTQ INPUT> <FASTA OUTPUT>

#from Bio.SeqIO.QualityIO import FastqGeneralIterator
#handle = open(sys.argv[2], 'w')
#for title, seq, qual in FastqGeneralIterator(open(sys.argv[1])):
#	handle.write(">%s\n%s\n" % (title, seq))
#handle.close()
from Bio import SeqIO
import sys

RECORD_BUFFER_SIZE = 1000000

file = open(sys.argv[2], 'w')
r_list = []
size = 0
for r in SeqIO.parse(sys.argv[1], "fastq"):
	r_list.append(r)
	size += 1
	if size == RECORD_BUFFER_SIZE: 
		SeqIO.write(r_list, file, "fasta")
		r_list = []
		size = 0
if size > 0: 
	SeqIO.write(r_list, file, "fasta")
file.close()
