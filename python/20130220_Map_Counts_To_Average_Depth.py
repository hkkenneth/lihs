# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20130220_Map_Counts_To_Average_Depth.py <COUNT> <LEN FILE> <OUT>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20130220_Map_Counts_To_Average_Depth.py to get usage'

total_count = 0
count_dict = {}
for line in open(sys.argv[1]):
	tokens = line.strip().split(" ")
	count = int(tokens[0])
	count_dict[tokens[1]] = count
	total_count += count
print total_count

outf = open(sys.argv[3], 'w')
total_avg_depth = 0.0
contig_count = 0
for line in open(sys.argv[2], 'r'):
	contig_count += 1
	tokens = line[:-1].split("\t")
	if tokens[0] in count_dict:
		avg_depth = count_dict[tokens[0]] * 50.0 / float(tokens[1])
		total_avg_depth += avg_depth
		outf.write("%s\t%s\n" % (tokens[0], str(avg_depth)))
	else:
		outf.write("%s\t0\n" % (tokens[0]))

print total_avg_depth / contig_count
outf.close()
