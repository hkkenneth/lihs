# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 30-11-2012
## Usage: python ~/code/python/025_Fasta_Split_By_Numbers.py <NUMBER PER OUTPUT> <INPUT FASTA ...>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/025_Fasta_Split_By_Numbers.py to get usage'

from Bio import SeqIO
l = int(sys.argv[1])
for s in sys.argv[2:]:
	count = 0
	filecount = 0
	records = []
	for record in SeqIO.parse(s, "fasta"):
		records.append(record)
		count += 1
		if (count == l):
			file = open(s+"." + str(filecount) + ".fa", 'w')
			SeqIO.write(records, file, "fasta")
			records = []
			count = 0
			filecount += 1
			file.close()
	if count > 0:
		file = open(s+"." + str(filecount) + ".fa", 'w')
		SeqIO.write(records, file, "fasta")
		file.close()	
