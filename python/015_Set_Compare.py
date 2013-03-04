# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 21-11-2012 
## Take a fasta file, can split the sequences into 2 files according to whether the id exists in the list
## for the in list output fasta file, the order is the same as the id list
## Usage: python ~/code/python/003_Fasta_Filter_By_IDs.py <ID LIST> <IN LIST OUTPUT FASTA> <OUT LIST OUTPUT FASTA> <INPUT FASTA ...>
## if the output fasta is not need, use "-"

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/003_Fasta_Filter_By_IDs.py to get usage'

set1 = set([])
for line in open(sys.argv[1], 'r'):
	set1.add(line[:-1])

set2 = set([])
for line in open(sys.argv[2], 'r'):
	set2.add(line[:-1])

print "In set 1 only: %i" % len(set1-set2)
print "In set 2 only: %i" % len(set2-set1)
print "In set both 1 and 2: %i" % len(set1 & set2)
print "In set either 1 and 2: %i" % len(set1 | set2)

