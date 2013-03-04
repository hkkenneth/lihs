# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 2013-01-02
## Usage: python ~/code/python/030_Fastq_Quality_Filter.py <READ 1 IN> <READ 2 IN> <READ 1 OUT> <READ 2 OUT>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/030_Fastq_Quality_Filter.py to get usage'
from Bio import SeqIO
import sys

dict1 = {'A' : 0, 'C' : 0, 'G' : 0, 'T' : 0 , 'S' : 0, 'Q' : 0}
dict2 = {'A' : 0, 'C' : 0, 'G' : 0, 'T' : 0 , 'S' : 0, 'Q' : 0}

def filter(seq, qual, dict):
	last = 'A'
	count = 0
	totalQual = 0
	continueCount = 0
	avgQual = 30 # in fact used for the first base only
	ok = True
	if len(seq) < 80:
		# too short
		dict['S'] += 1
		ok = False
	else:
		for c in seq:
			thisQual = qual[count]
			count += 1
			if (c == 'N') or (thisQual < avgQual - 5) or (c == last):
				continueCount += 1
			else:
				continueCount = 1
				last = c			
			if (continueCount >= 60) or (continueCount == len(seq)):
				dict[last] += 1
				ok = False
				break
			totalQual += thisQual
			avgQual = totalQual / count
			if (count == 80) and (avgQual < 30):
				dict['Q'] += 1
				ok = False
				break
	return ok

def trimAndWrite(rec, file):
	SeqIO.write([rec], file, "fastq")

f1pair = open(sys.argv[3] + ".pair.fastq", 'w')
f2pair = open(sys.argv[4] + ".pair.fastq", 'w')
f1single = open(sys.argv[3] + ".single.fastq", 'w')
f2single = open(sys.argv[4] + ".single.fastq", 'w')
fstat = open(sys.argv[3] + ".stat", 'w')

seqcount = 0
bothpass=0
pass1=0
pass2=0
read2s = SeqIO.parse(sys.argv[2], "fastq")
for r1 in SeqIO.parse(sys.argv[1], "fastq"):
	r2 = read2s.next()
	seqcount += 1
	passFilter1 = filter(r1.seq, r1.letter_annotations["phred_quality"], dict1)
	passFilter2 = filter(r2.seq, r2.letter_annotations["phred_quality"], dict2)
	if passFilter1 and passFilter2:
		trimAndWrite(r1, f1pair)
		trimAndWrite(r2, f2pair)
		bothpass += 1
	elif passFilter1:
		trimAndWrite(r1, f1single)
		pass1 += 1
	elif passFilter2:
		trimAndWrite(r2, f2single)
		pass2 += 1
#	if seqcount == 100000:
#		break
fstat.write("Total seq: %i\n" % seqcount)
fstat.write("Both pass: %i\n" % bothpass)
fstat.write("Singleton in  read 1: %i\n" % pass1)
fstat.write("Singleton in  read 2: %i\n" % pass2)
fstat.write("Both failed: %i\n" % abs(seqcount - bothpass - pass1 - pass2))
fstat.write(str(dict1) + "\n")
fstat.write(str(dict2) + "\n\n")

fstat.write("Read 1\n%i\n\n%i\n\n%i\n\n%i\n\n%i\n\n%i\n\n" % (dict1['A'], dict1['C'] + dict1['G'] + dict1['T'], dict1['Q'], dict1['S'], pass1, bothpass))
fstat.write("Read 2\n%i\n\n%i\n\n%i\n\n%i\n\n%i\n\n%i\n\n" % (dict2['A'], dict2['C'] + dict2['G'] + dict2['T'], dict2['Q'], dict2['S'], pass2, bothpass))
