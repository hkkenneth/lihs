# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 01-11-2012 
## Take a fasta file, can split the sequences into 2 files according to whether the id exists in the list
## for the in list output fasta file, the order is the same as the id list
## Usage: python ~/code/python/003_Fasta_Filter_By_IDs.py <ID LIST> <IN LIST OUTPUT FASTA> <OUT LIST OUTPUT FASTA> <INPUT FASTA ...>
## if the output fasta is not need, use "-"

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/003_Fasta_Filter_By_IDs.py to get usage'

from Bio import SeqIO

RECORD_BUFFER_SIZE = 100000

name_set = set([])
name_list = []
for line in open(sys.argv[1], 'r'):
	id = line[:-1].strip()
	if id not in name_set:
		name_set.add(id)
		name_list.append(id)

if sys.argv[2] == "-":
	f1 = None
else:
	f1 = open(sys.argv[2], 'w')

if sys.argv[3] == "-":
	f2 = None
else:
	f2 = open(sys.argv[3], 'w')

r_dict = {}

r_list = []
size = 0

for s in sys.argv[4:]:
	for record in SeqIO.parse(s, "fasta"):
		if record.id in name_set:
			if f1 is not None:
				r_dict[record.id] = record
		elif f2 is not None:
			size += 1
			r_list.append(record)
			if size == RECORD_BUFFER_SIZE: 
				SeqIO.write(r_list, f2, "fasta")
				r_list = []
				size = 0
if size > 0: 
	SeqIO.write(r_list, f2, "fasta")

r_list = []

for name in name_list:
	if name in r_dict:
		r_list.append(r_dict[name])

if f1 is not None:
	SeqIO.write(r_list, f1, "fasta")
	f1.close()

if f2 is not None:
	f2.close()
