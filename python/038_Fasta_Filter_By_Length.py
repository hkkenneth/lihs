# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/038_Fasta_Filter_By_Length.py <FASTA IN> <LENGTH VALUES ...>
# Take a fasta file, can split the sequences into multiple files according to the length

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/038_Fasta_Filter_By_Length.py to get usage'
from Bio import SeqIO

len_list = [ int(s) for s in sys.argv[2:] ]
len_list.sort(reverse=True)
len_list.append(0)

fileDict = {}
for j in len_list:
	fileDict[j] = open(sys.argv[1] + "." + str(j) + "bp_or_above", 'w')
for record in SeqIO.parse(sys.argv[1], "fasta"):
	l = len(record.seq)
	for i in len_list:
		if l >= i:
			SeqIO.write([record], fileDict[i], "fasta")
			break
for j in len_list:
	fileDict[j].close()
