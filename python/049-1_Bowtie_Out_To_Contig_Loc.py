# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 03-03-2013 
## Usage: python ~/code/python/049-1_Bowtie_Out_To_Contig_Loc.py <INPUT> <LEN> <OUTPUT PREFIX>
## Useful command: sort -k 2 -t $'\t' <OUTPUT PREFIX>.py049-1.out

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/049-1_Bowtie_Out_To_Contig_Loc.py to get usage'

outf = open(sys.argv[3] + ".py049-1.out", 'w')

len_dict = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	read_id = tokens[0]
	contig_id = tokens[2]
	pos = int(tokens[3])
	status = "MIDDLE"
	if pos < 1000:
		status = "L_END"
	elif pos > len_dict[contig_id] - 1000:
		status = "R_END"
	outf.write("%s\t%s\t%s\t%i\n" % (read_id, contig_id, status, pos))

outf.close()
