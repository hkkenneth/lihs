# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 07-01-2013
## Usage: python ~/code/python/001c_Fastq_Trimming_5end_only.py <FIRST BASE> <FASTQ 1> <FASTQ 2>
## Bases are inclusive and 1-based

import sys

start = int(sys.argv[1]) - 1

s1 = sys.argv[2]
s2 = sys.argv[3]
file1 = open(s1 + "." + sys.argv[1] + "-end.trimmed.fastq", 'w')
file2 = open(s2 + "." + sys.argv[1] + "-end.trimmed.fastq", 'w')
file1d = open(s1 + "." + sys.argv[1] + "-end.discarded.fastq", 'w')
file2d = open(s2 + "." + sys.argv[1] + "-end.discarded.fastq", 'w')


lines1 = open(s1, 'r').readlines()
lines2 = open(s2, 'r').readlines()
temp = [3, 2, 1, 0]
i = 0
for line in lines1:
	if i % 4 == 3:
		if (len(line)-1 > start) and (len(lines2[i])-1 > start):
			file1.write(lines1[i - 3])
			file1.write("%s\n" % lines1[i - 2][start:])
			file1.write(lines1[i - 1])
			file1.write("%s\n" % lines1[i][start:])

			file2.write(lines2[i - 3])
			file2.write("%s\n" % lines2[i - 2][start:])
			file2.write(lines2[i - 1])
			file2.write("%s\n" % lines2[i][start:])
		else:
			for j in temp:
				file1d.write(lines1[i - j])
				file2d.write(lines2[i - j])
	i = i + 1

file1.close()
file2.close()
file1d.close()
file2d.close()
