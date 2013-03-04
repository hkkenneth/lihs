# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 06-12-2012
## Usage: python ~/code/python/20121206_May_Paper_Seq_To_Fasta_With_Gene_Symbol.py <INPUT> <OUTPUT> <LIST OF SYMBOL>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121206_May_Paper_Seq_To_Fasta_With_Gene_Symbol.py to get usage'

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

symbols = set([])
for line in open(sys.argv[3], 'r'):
	symbols.add(line[:-1])

outf = open(sys.argv[2], 'w')
for line in open(sys.argv[1], 'r'):
	# use -2 because the line break is strange..
	tokens = line[:-2].split("\t")
	if tokens[1].upper() in symbols:
		record = SeqRecord(Seq(tokens[2], IUPAC.IUPACAmbiguousDNA), id=(tokens[0] + "_" + tokens[1]), description="")
		SeqIO.write(record, outf, "fasta")

outf.close()
