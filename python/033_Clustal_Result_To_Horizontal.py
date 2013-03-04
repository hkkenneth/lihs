# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/033_Clustal_Result_To_Horizontal.py <IN> <OUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/033_Clustal_Result_To_Horizontal.py to get usage'

outf = open(sys.argv[2], 'w')
lcount = 0
lindex = 0
first = True
outlist = []
for line in open(sys.argv[1], 'r'):
	lcount += 1
	if lcount <= 3 :
		continue
	if len(line) == 1:
		first = False
		lindex = 0
	else: 
		if first:
			outlist.append(line[:-1])
		else:
			if not outlist[lindex].startswith(line[:36]):
				print "problem!"
			outlist[lindex] = outlist[lindex] + line[36:-1]
		lindex += 1

print len(outlist)
for line in outlist:
	outf.write("%s\n" % line)
outf.close()
