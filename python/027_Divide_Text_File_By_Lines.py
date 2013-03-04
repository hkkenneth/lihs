# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/027_Divide_Text_File_By_Lines.py <NUMBER OF LINES> <FILES ...>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/027_Divide_Text_File_By_Lines.py to get usage'

l = int(sys.argv[1])

for file_name in sys.argv[2:]:
	file_count = 0
	lines = []
	line_count = 0
	for line in open(file_name, 'r'):
		line_count += 1
		lines.append(line)
		if line_count == l:
			file_count += 1
			outf = open(file_name + "." + str(file_count), 'w')
			outf.writelines(lines)
			outf.close()
			lines = []
			line_count = 0
	if line_count > 0:
		file_count += 1
		outf = open(file_name + "." + str(file_count), 'w')
		outf.writelines(lines)
		outf.close()

