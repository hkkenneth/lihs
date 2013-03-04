# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 12-11-2012
## Usage: python ~/code/python/009_Fasta_Find_ORF.py <FASTA FILE> <MIN PROTEIN LENGTH (e.g. 60)>
## Output files: <FASTA FILE>.orf.middle	<FASTA FILE>.orf.first	<FASTA FILE>.orf.last
## Output files: <FASTA FILE>.rev.orf.middle	<FASTA FILE>.rev.orf.first	<FASTA FILE>.rev.orf.last

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/009_Fasta_Find_ORF.py to get usage'

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

def write_forward(i, prot, r, f, min_len):
	if len(prot) >= min_len:
		cds_str = "_" + str(i+1) + "-" + str(i + len(prot)*3)
		record = SeqRecord(prot, id=r.id + cds_str, name=r.id + cds_str, description="")
		SeqIO.write([record], f, "fasta")

def write_reverse(i, prot, r, f, min_len):
	if len(prot) >= min_len:
		cds_str = "_" + str(i) + "-" + str(i - len(prot)*3 + 1)
		record = SeqRecord(prot, id=r.id + cds_str, name=r.id + cds_str, description="")
		SeqIO.write([record], f, "fasta")

f1 = open(sys.argv[1] + ".orf.middle", 'w')
f2 = open(sys.argv[1] + ".orf.first", 'w')
f3 = open(sys.argv[1] + ".orf.last", 'w')

f4 = open(sys.argv[1] + ".rev.orf.middle", 'w')
f5 = open(sys.argv[1] + ".rev.orf.first", 'w')
f6 = open(sys.argv[1] + ".rev.orf.last", 'w')


MIN_PROT_LEN = int(sys.argv[2])

for r in SeqIO.parse(sys.argv[1], "fasta"):
	for i in range(3):
		frame = r.seq[i:].translate(1)
		prots = frame.split('*')
		if len(prots) == 1:
			write_forward(i, prots[0], r, f2, MIN_PROT_LEN)
		elif len(prots) == 2:
			write_forward(i, prots[0], r, f2, MIN_PROT_LEN)
			offset = len(prots[0]) * 3 + 3 + i	# zero based
			write_forward(offset, prots[1], r, f3, MIN_PROT_LEN)
		else:
			write_forward(i, prots[0], r, f2, MIN_PROT_LEN)
			offset = len(prots[0]) * 3 + 3 + i	# zero based
			for prot in prots[1:-1]:
				write_forward(offset, prot, r, f1, MIN_PROT_LEN)
				offset += len(prot) * 3 + 3	# zero based
			write_forward(offset, prots[-1], r, f3, MIN_PROT_LEN)

	for i in range(3):
		frame = r.seq.reverse_complement()[i:].translate(1)
		prots = frame.split('*')
		l = len(r.seq)
		if len(prots) == 1:
			write_reverse(l-i, prots[0], r, f5, MIN_PROT_LEN)
		elif len(prots) == 2:
			write_reverse(l-i, prots[0], r, f5, MIN_PROT_LEN)
			offset = l - i - len(prots[0]) * 3 - 3	# zero based
			write_reverse(offset, prots[1], r, f6, MIN_PROT_LEN)
		else:
			write_reverse(l-i, prots[0], r, f5, MIN_PROT_LEN)
			offset = l - i - len(prots[0]) * 3 - 3	# zero based
			for prot in prots[1:-1]:
				write_reverse(offset, prot, r, f4, MIN_PROT_LEN)
				offset -= (len(prot) * 3 + 3)	# zero based
			write_reverse(offset, prots[-1], r, f6, MIN_PROT_LEN)

f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
