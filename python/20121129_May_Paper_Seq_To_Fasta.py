# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 29-11-2012
## Usage: python ~/code/python/20121129_May_Paper_Seq_To_Fasta.py <INPUT> <OUTPUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121129_May_Paper_Seq_To_Fasta.py to get usage'

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
outf = open(sys.argv[2], 'w')
for line in open(sys.argv[1], 'r'):
	# use -2 because the line break is strange..
	tokens = line[:-2].split("\t")
	record = SeqRecord(Seq(tokens[1], IUPAC.IUPACAmbiguousDNA), id=tokens[0], description="")
	SeqIO.write(record, outf, "fasta")

outf.close()
