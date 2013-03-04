# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/047-2A_Mpileup_Highlight_To_GFF_UniqUniqSame.py <INPUT FILE> <OUTPUT PREFIX> <FEATURE NAME> <CUTOFF VALUE> <RANGE>

import sys
if len(sys.argv) < 6:
        raise SystemExit, 'use grep "##" ~/code/python/047-2A_Mpileup_Highlight_To_GFF_UniqUniqSame.py to get usage'

cutf = open(sys.argv[2] + '.py047-2a.cut_site.gff3', 'w')
logf = open(sys.argv[2] + '.py047-2a.log', 'w')
logf.write("Parameters:\n")

fea_name = sys.argv[3]
cut_off = float(sys.argv[4])
cut_range = int(sys.argv[5])
logf.write("Feature Name:\t%s\n" % fea_name)
logf.write("Cutoff:\t%s\n" % sys.argv[4])
logf.write("Cut Range:\t%i\n" % cut_range)

seq_id = ""
start = -1
for line in open(sys.argv[1]):
	tokens = line.split("\t")
	if (tokens[0] == seq_id) and (int(tokens[1]) == end + 1):
		depth += int(tokens[3])
		end += 1
	else:
		if start != -1:
			avg_depth = float(depth) / (end - start + 1)
			if avg_depth >= cut_off:
				mid = (start + end ) / 2
				new_start = max(mid - cut_range, 1)
				new_end = mid + cut_range
				cutf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i_%i\n" % (seq_id, fea_name, new_start, new_end, seq_id, new_start, new_end))
		seq_id = tokens[0]
		start = int(tokens[1])
		end = int(tokens[1])
		depth = int(tokens[3])
cutf.close()
