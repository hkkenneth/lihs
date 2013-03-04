# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012 
## Usage: python ~/code/python/002_Fasta_Add_Prefix.py <INPUT FASTA> <PREFIX> <OUTPUT FASTA>

from Bio import SeqIO
import sys
if len(sys.argv) < 4:
	raise SystemExit, 'use grep "##" ~/code/python/002_Fasta_Add_Prefix.py to get usage'

RECORD_BUFFER_SIZE = 100000

ohandle=open(sys.argv[3], 'w')

r_list = []
size = 0

for record in SeqIO.parse(sys.argv[1], "fasta"):
	record.description = record.description[(len(record.id) + 1):]
	record.id = sys.argv[2] + record.id.replace(".", "-")
	r_list.append(record)
	size += 1
	if size == RECORD_BUFFER_SIZE: 
		SeqIO.write(r_list, ohandle, "fasta")
		r_list = []
		size = 0
if size > 0: 
	SeqIO.write(r_list, ohandle, "fasta")

ohandle.close()
