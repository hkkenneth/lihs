# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 15-11-2012
## Usage: python ~/code/python/20121115_Verify_CDS.py <SEQ FASTA> <LIST>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121115_Verify_CDS.py to get usage'

from Bio import SeqIO
import sys
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

record_dict = SeqIO.index(sys.argv[1], "fasta")

count = 0
for line in open(sys.argv[2], 'r'):
	tokens = line.split("\t")
	id = tokens[0]
	start = int(tokens[5])-1
	end = int(tokens[3])-1
	r = record_dict[id]
	if start < 0:
		print "%s\t-1" % id
		continue
	if start < end:
		subseq = r.seq[start:end+1]
	else:
		subseq = r.seq[end:start+1].reverse_complement()
	tran_seq = subseq.translate(1)
	if (tran_seq[0] != 'M'):
		print id
		print tran_seq[:10]
