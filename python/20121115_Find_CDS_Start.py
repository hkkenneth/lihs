# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 15-11-2012
## Usage: python ~/code/python/20121115_Find_CDS_Start.py <INPUT LIST> <ORF FASTA> <OUTPUT>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121115_Find_CDS_Start.py to get usage'

from Bio import SeqIO

fasta_dict = {}
for r in SeqIO.parse(sys.argv[2], 'fasta'):
	fasta_dict[r.id] = str(r.seq)

outf1 = open(sys.argv[3], 'w')
logf = open(sys.argv[3] + "1115.CDS.log", 'w')

for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	q_r = tokens[6].split("-")
	s_r = tokens[7].split("-")
	q_start = int(q_r[0])
	s_start = int(s_r[0])
	# new_q_start is the expected starting pos of CDS on the ORF, 1-based.
	new_q_start = q_start - s_start + 1
	cds_start = -1
	if new_q_start <= 0:
		logf.write("%s\tIncomplete\tExpected: %i\n" % (tokens[0], new_q_start))
		new_q_start = 1
	seq = fasta_dict[tokens[0]]
	m_index = seq[:new_q_start].rfind("M")
	orf_r = tokens[0][tokens[0].rfind("_")+1:].split("-")
	orf_start = int(orf_r[0])
	orf_end = int(orf_r[1])
	if m_index < 0:
		m_index = seq.find("M")
	if m_index >= 0:
		# m_index is the pos of "M" which starts the CDS, 0-based.
		if orf_start < orf_end:
			cds_start = orf_start + (m_index * 3)
		else:
			cds_start = orf_start - (m_index * 3)
	else:
		logf.write("%s\tno m at all\n" % tokens[0])
	outf1.write("%i\n" % cds_start)

outf1.close()
logf.close()
