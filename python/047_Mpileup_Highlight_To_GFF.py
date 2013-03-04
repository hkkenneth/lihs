# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/047_Mpileup_Highlight_To_GFF.py <INPUT FILE> <OUTPUT PREFIX> <FEATURE NAME> <CUTOFF VALUE>

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/047_Mpileup_Highlight_To_GFF.py to get usage'

badf = open(sys.argv[2] + '.py047.highlight_bad.gff3', 'w')
logf = open(sys.argv[2] + '.py047.log', 'w')

fea_name = sys.argv[3]
cut_off = float(sys.argv[4])
logf.write("Parameters:\n")
logf.write("Feature Name:\t%s\n" % fea_name)
logf.write("Cutoff:\t%s\n" % sys.argv[4])

seq_id = ""
start = -1
bad_site_count = 0
bad_site_size = 0
for line in open(sys.argv[1]):
	tokens = line.split("\t")
	if (tokens[0] == seq_id) and (int(tokens[1]) == end + 1):
		depth += int(tokens[3])
		end += 1
	else:
		if start != -1:
			avg_depth = float(depth) / (end - start + 1)
			avg_depth_str = str(float(depth) / (end - start + 1))[:5]
			if avg_depth >= cut_off:
				badf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i_%s\n" % (seq_id, fea_name, start, end, seq_id, start, avg_depth_str))
				bad_site_size += end - start + 1
				bad_site_count += 1
			logf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i_%s\t%i\n" % (seq_id, fea_name, start, end, seq_id, start, avg_depth_str, (end - start + 1)))
		seq_id = tokens[0]
		start = int(tokens[1])
		end = int(tokens[1])
		depth = int(tokens[3])
logf.write("Average Bad Site Size:%s\n" % (float(bad_site_size) / bad_site_count))
logf.write("Bad Site Count:%i\n" % bad_site_count)
logf.close()
badf.close()
