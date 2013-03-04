# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 19-01-2013
## Usage: python ~/code/python/035_Fasta_Translate_6_Frames.py <FASTA FILE IN> <FASTA FILE OUT>
import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/009_Fasta_Find_ORF.py to get usage'

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

f1 = open(sys.argv[2], 'w')

for r in SeqIO.parse(sys.argv[1], "fasta"):
	for i in range(3):
		frame = r.seq[i:].translate(1)
		record = SeqRecord(frame, id=r.id + "_+" + str(i+1), name=r.id + "_+" + str(i+1), description="")
		SeqIO.write([record], f1, "fasta")

	for i in range(3):
		frame = r.seq.reverse_complement()[i:].translate(1)
		record = SeqRecord(frame, id=r.id + "_-" + str(i+1), name=r.id + "_-" + str(i+1), description="")
		SeqIO.write([record], f1, "fasta")

f1.close()
