# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 28-01-2013
## Usage: python ~/code/python/040_Fasta_Sort_By_Length_And_Split.py <OUTPUT PREFIX> <BASES PER FILE> <MAX NO. OF FILES | - > <INPUT FASTA FILES ...>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/040_Fasta_Sort_By_Length_And_Split.py to get usage'

rec_dict = {}
from Bio import SeqIO
for s in sys.argv[4:]:
	for rec in SeqIO.parse(s, "fasta"):
		if len(rec.seq) in rec_dict:
			rec_dict[len(rec.seq)].append(rec)
		else:
			rec_dict[len(rec.seq)] = [rec]

blimit = int(sys.argv[2])
flimit = 100000000
if sys.argv[3] != "-" :
	flimit = int(sys.argv[3])

klist = rec_dict.keys()
klist.sort(reverse=True)
fcount = 0
bcount = 0
rec_list = []
logf = open(sys.argv[1] + ".py040.log", 'w')
stop = False
for k in klist:
	for rec in rec_dict[k]:
		rec_list.append(rec)
		bcount += len(rec.seq)
		if bcount >= blimit:
			logf.write("%s.%i.fa written, length cutoff: %i\n" % (sys.argv[1], fcount, len(rec.seq)))
			outf = open(sys.argv[1] + "." + str(fcount) + ".fa", 'w')
			SeqIO.write(rec_list, outf, "fasta")
			rec_list = []
			bcount = 0
			outf.close()
			fcount += 1 
			if fcount >= flimit:
				stop = True
				break
	if stop:
		break
if bcount > 0:
	logf.write("%s.%i.fa written, length cutoff: %i\n" % (sys.argv[1], fcount, len(rec.seq)))
	outf = open(sys.argv[1] + "." + str(fcount) + ".fa", 'w')
	SeqIO.write(rec_list, outf, "fasta")
	outf.close()

logf.close()
