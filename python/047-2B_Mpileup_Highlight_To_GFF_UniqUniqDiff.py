# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/047-2B_Mpileup_Highlight_To_GFF_UniqUniqDiff.py <INPUT FILE> <REF LEN> <OUTPUT PREFIX>  <FEATURE NAME> <CUTOFF VALUE> <RANGE>

import sys
if len(sys.argv) < 7:
        raise SystemExit, 'use grep "##" ~/code/python/047-2B_Mpileup_Highlight_To_GFF_UniqUniqDiff.py to get usage'

len_dict = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	len_dict[tokens[0]] = int(tokens[1])

cutf = open(sys.argv[3] + '.py047-2b.cut_site.gff3', 'w')
logf = open(sys.argv[3] + '.py047-2b.log', 'w')

logf.write("Parameters:\n")

fea_name = sys.argv[4]
cut_off = float(sys.argv[5])
cut_range = int(sys.argv[6])
logf.write("Feature Name:\t%s\n" % fea_name)
logf.write("Cutoff:\t%s\n" % sys.argv[5])
logf.write("Cut Range:\t%i\n" % cut_range)

seq_id = ""
start = -1
for line in open(sys.argv[1]):
	tokens = line.split("\t")
	if len_dict[tokens[0]] < 1000:
		continue
	if int(tokens[1]) <= 1000:
		continue
	if int(tokens[1])+1000 > len_dict[tokens[0]]:
		if start != -1:
			avg_depth = float(depth) / (end - start + 1)
			if avg_depth >= cut_off:
				new_start = max(start - cut_range, 1)
				new_end = min(start + cut_range, len_dict[seq_id])
				cutf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i_%i\n" % (seq_id, fea_name, new_start, new_end, seq_id, new_start, new_end))
				id1 = "%s_%i_%i" % (seq_id, new_start, new_end)
				new_start = max(end - cut_range, 1)
				new_end = min(end + cut_range, len_dict[seq_id])
				cutf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i_%i\n" % (seq_id, fea_name, new_start, new_end, seq_id, new_start, new_end))
				id2 = "%s_%i_%i" % (seq_id, new_start, new_end)
				logf.write("%s\t%s\n" % (id1, id2))
		
		start = -1
		continue
	if (tokens[0] == seq_id) and (int(tokens[1]) == end + 1):
		depth += int(tokens[3])
		end += 1
	else:
		if start != -1:
			avg_depth = float(depth) / (end - start + 1)
			if avg_depth >= cut_off:
				new_start = max(start - cut_range, 1)
				new_end = min(start + cut_range, len_dict[seq_id])
				cutf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i_%i\n" % (seq_id, fea_name, new_start, new_end, seq_id, new_start, new_end))
				id1 = "%s_%i_%i" % (seq_id, new_start, new_end)
				new_start = max(end - cut_range, 1)
				new_end = min(end + cut_range, len_dict[seq_id])
				cutf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i_%i\n" % (seq_id, fea_name, new_start, new_end, seq_id, new_start, new_end))
				id2 = "%s_%i_%i" % (seq_id, new_start, new_end)
				logf.write("%s\t%s\n" % (id1, id2))
		seq_id = tokens[0]
		start = int(tokens[1])
		end = int(tokens[1])
		depth = int(tokens[3])
cutf.close()
logf.close()
