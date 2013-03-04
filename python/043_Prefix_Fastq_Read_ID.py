# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 04-02-2013 
## Usage: python ~/code/python/043_Prefix_Fastq_Read_ID.py <IN> <PREFIX> <OUT>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/043_Prefix_Fastq_Read_ID.py to get usage'

import sys
fout = open(sys.argv[3], 'w')
fin = open(sys.argv[1], 'r')
line_count = 0
for line in fin:
	if line_count == 0:
		fout.write("@%s%s" % (sys.argv[2], line[1:]))
	else:
		fout.write(line)
	line_count = (line_count + 1) % 4
fout.close()
fin.close()
