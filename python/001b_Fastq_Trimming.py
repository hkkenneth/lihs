# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 10-12-2012
## Usage: python ~/code/python/001b_Fastq_Trimming.py <FIRST BASE> <LAST BASE> <FASTQ FILES....>
## Bases are inclusive and 1-based

import sys

start = int(sys.argv[1]) - 1
end = int(sys.argv[2])

s1 = sys.argv[3]
s2 = sys.argv[4]
file1 = open(s1 + "." + sys.argv[1] + "-" + sys.argv[2] + ".trimmed", 'w')
file2 = open(s2 + "." + sys.argv[1] + "-" + sys.argv[2] + ".trimmed", 'w')
file1d = open(s1 + "." + sys.argv[1] + "-" + sys.argv[2] + ".discarded", 'w')
file2d = open(s2 + "." + sys.argv[1] + "-" + sys.argv[2] + ".discarded", 'w')

lines1 = []
lines2 = []
count = 0
temp = [0, 1, 2, 3]
reads_count = 0
in_f2 = open(s2, 'r')
for line in open(s1, 'r'):
	lines1.append(line)
	lines2.append(in_f2.readline())
	count += 1
	if count == 4:
		if (len(lines1[1]) < end+1) or (len(lines2[1]) < end+1):
			for i in temp:
				file1d.write(lines1[i])
				file2d.write(lines2[i])
		else:
			file1.write(lines1[0])
			file1.write("%s\n" % lines1[1][start:end])
			file1.write(lines1[2])
			file1.write("%s\n" % lines1[3][start:end])
			file2.write(lines2[0])
			file2.write("%s\n" % lines2[1][start:end])
			file2.write(lines2[2])
			file2.write("%s\n" % lines2[3][start:end])
		lines1 = []
		lines2 = []
		count = 0

file1.close()
file2.close()
file1d.close()
file2d.close()
