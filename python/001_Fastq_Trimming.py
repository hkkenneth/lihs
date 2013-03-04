# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012
## Usage: python ~/code/python/001_Fastq_Trimming.py <FIRST BASE> <LAST BASE> <FASTQ FILES....>
## Bases are inclusive and 1-based

#from Bio.SeqIO.QualityIO import FastqGeneralIterator
#handle = open(sys.argv[2], 'w')
#for title, seq, qual in FastqGeneralIterator(open(sys.argv[1])):
#       handle.write("@%s\n%s\n+\n%\n" % (title, seq[...:...], qual[...:...]))
#handle.close()

from Bio import SeqIO
import sys

RECORD_BUFFER_SIZE = 100000

start = int(sys.argv[1]) - 1
end = int(sys.argv[2])

for s in sys.argv[3:]:
	file = open(s + "." + sys.argv[1] + "-" + sys.argv[2] + ".trimmed", 'w')
	r_list = []
	size = 0
	for r in SeqIO.parse(s, "fastq"):
		r_list.append(r[start:end])
		size += 1
		if size == RECORD_BUFFER_SIZE: 
			SeqIO.write(r_list, file, "fastq")
			r_list = []
			size = 0
	if size > 0: 
		SeqIO.write(r_list, file, "fastq")
	file.close()
