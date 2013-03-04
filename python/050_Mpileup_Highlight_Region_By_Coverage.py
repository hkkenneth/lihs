# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 03-03-2013 
## Usage: python ~/code/python/050_Mpileup_Highlight_Region_By_Coverage.py <INPUT FILE> <OUTPUT PREFIX>  <FEATURE NAME> <CUTOFF VALUE> <MIN LEN>

import sys
if len(sys.argv) < 6:
        raise SystemExit, 'use grep "##" ~/code/python/050_Mpileup_Highlight_Region_By_Coverage.py to get usage'

cutf = open(sys.argv[2] + '.py050.cut_site.gff3', 'w')
logf = open(sys.argv[2] + '.py050.log', 'w')

logf.write("Parameters:\n")

fea_name = sys.argv[3]
cut_off = float(sys.argv[4])
min_len = int(sys.argv[5])
logf.write("Feature Name:\t%s\n" % fea_name)
logf.write("Cutoff:\t%s\n" % sys.argv[4])
logf.write("Min Len:\t%s\n" % sys.argv[5])

seq_id = ""
start = -1
end = -1
for line in open(sys.argv[1]):
	tokens = line.split("\t")
	if int(tokens[3]) > cut_off:
		if (seq_id == tokens[0]) and (int(tokens[1]) == end + 1):
			depth = max(depth, int(tokens[3]))
			end += 1
		else:
			if ((end-start+1)>min_len) and ( seq_id != ""):
				cutf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i\n" % (seq_id, fea_name, start, end, seq_id, depth))
			seq_id = tokens[0]
			start = int(tokens[1])
			end = int(tokens[1])
			depth = int(tokens[3])
	else:
		if ((end-start+1)>min_len) and ( seq_id != ""):
			cutf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i\n" % (seq_id, fea_name, start, end, seq_id, depth))
		seq_id = ""
if ((end-start+1)>min_len) and ( seq_id != ""):
	cutf.write("%s\t.\t%s\t%i\t%i\t.\t+\t.\tID=%s_%i\n" % (seq_id, fea_name, start, end, seq_id, depth))
cutf.close()
logf.close()
