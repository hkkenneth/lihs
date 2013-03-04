# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 29-Nov-2012 
## Usage: python ~/code/python/023_Text_File_To_Upper_Case.py <IN> <OUT>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/023_Text_File_To_Upper_Case.py to get usage'

outf = open(sys.argv[2], 'w')

for line in open(sys.argv[1], 'r'):
	outf.write(line.upper())

outf.close()
