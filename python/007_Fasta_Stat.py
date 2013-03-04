# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/007_Fasta_Stat.py <FASTA> <VALUES ... e.g.  500 2000 10000 40000>

import sys
if len(sys.argv) < 2:
        raise SystemExit, 'use grep "##" ~/code/python/007_Fasta_Stat.py to get usage'

from Bio import SeqIO

cutoff = [int(x) for x in sys.argv[2:]]
cutoff.sort()
smaller_count = {}
for c in cutoff:
	smaller_count[c] = 0

count = 0
maxL = 0
minL = -1
sumL = 0

f = open(sys.argv[1] + ".python007.stat", 'w')
f2 = open(sys.argv[1] + ".python007.len", 'w')
lenList = []

for record in SeqIO.parse(sys.argv[1], "fasta"):
	l = len(record.seq)
	for c in cutoff:
		if l <= c:
			smaller_count[c] += 1
		else:
			continue
	lenList.append(l)
	if minL == -1:
		minL = l
	f2.write("%s\t%i\n" % (record.id, l))
	count = count + 1
	maxL = max(maxL, l)
	minL = min(minL, l)
	sumL = sumL + l
	
tempSum = 0
n50 = 0
l1 = list(reversed(sorted(lenList)))
for i in l1:
	tempSum += i
	if (sumL / tempSum) < 2:
		n50 = i
		break
f.write("Number of sequences\t%i\n" % count)
f.write("Number of bases\t%i\n" % sumL)
f.write("Average length\t%i\n" % (sumL / count))
f.write("Maximum length\t%i\n" % maxL)
f.write("Minimum length\t%i\n" % minL)
f.write("N50 length\t%i\n" % n50)
f.write("Median length\t%i\n" % l1[len(l1)/2])
if len(cutoff) > 0:
	s1 = ""
	s2 = ""
	s3 = ""
	s4 = ""
	prev = 0
	prev_c = 0
	for c in cutoff:
		s1 = s1 + "\t" + str(c)
		s2 = s2 + "\t" + str(smaller_count[c])
		s3 = s3 + "\t" + str(prev_c+1) + "-" + str(c)
		s4 = s4 + "\t" + str(smaller_count[c] - prev)
		prev = smaller_count[c]
		prev_c = c
	f.write("\nAccumulated\n%s\n%s\n\nBand\n%s\n%s\n" % (s1, s2, s3, s4))
f.close()
f2.close()
