# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 13-12-2012
## Usage: python ~/code/python/20121213_Protein_Verify_Full_Length.py <TRANSCRIPT INPUT> <PROTEIN INPUT> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121213_Protein_Verify_Full_Length.py to get usage'

from Bio import SeqIO
rec_dict = {}
for r in SeqIO.parse(sys.argv[1], "fasta"):
	rec_dict[r.id] = r

p_outf = open(sys.argv[3] + ".protein_id", 'w')
t_outf = open(sys.argv[3] + ".transcript_id", 'w')
logf = open(sys.argv[3] + ".log", 'w')

frame = [1, 2, 3, -1, -2, -3]
for r in SeqIO.parse(sys.argv[2], "fasta"):
	t_id = r.id[:r.id.rfind("_")]
	t_rec = rec_dict[t_id]
	count = 0
	for f in frame:
		if f > 0:
			trans_seq = t_rec.seq[(f-1):].translate(1)
		else:
			trans_seq = t_rec.seq.reverse_complement()[(abs(f)-1):].translate(1)
		pos = trans_seq.find(r.seq)
		if (pos >= 0):
			if (pos + len(r.seq) < len(trans_seq)):
				if trans_seq[pos + len(r.seq)] == '*':
					p_outf.write("%s\n" % r.id)
					t_outf.write("%s\n" % t_id)
				else:
					logf.write("%s ends with %s instead (frame: %i)\n" % (t_id, trans_seq[pos + len(r.seq)], f))
			else:
				logf.write("%s ends at the end of contig (frame: %i)\n" % (r.id, f))
		else:
			count += 1
	if count == 6:
		logf.write("%s cannot be found in all frames\n" % r.id)

p_outf.close()
t_outf.close()
logf.close()
