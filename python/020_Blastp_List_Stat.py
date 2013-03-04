# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 27-11-2012
## Usage: python ~/code/python/020_Blastp_List_Stat.py <ID LIST> <BLASTP RESULT LIST> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/020_Blastp_List_Stat.py to get usage'


id_dict = {}
for line in open(sys.argv[1], 'r'):
	id_dict[line[:-1]] = set([])

logf = open(sys.argv[3] + ".log", 'w')
no_hit_ids = open(sys.argv[3] + ".no_hit.id", 'w')
single_hit_ids = open(sys.argv[3] + ".single_hit.id", 'w')
multi_hit_ids = open(sys.argv[3] + ".multi_hit.id", 'w')

for line in open(sys.argv[2], 'r'):
	tokens = line.split("\t")
	seq_id = tokens[0][:tokens[0].rfind("_")]
	id_dict[seq_id].add(tokens[0])

no_hit = 0
single_orf = 0
multi_orf = 0

for k in id_dict.keys():
	if len(id_dict[k]) == 0:
		no_hit_ids.write("%s\n" % k)
		no_hit += 1
	elif len(id_dict[k]) == 1:
		single_hit_ids.write("%s\n" % k)
		single_orf += 1
	else:
		multi_hit_ids.write("%s\n" % k)
		multi_orf += 1

logf.write("Total Number of Seq: %i\n" % len(id_dict.keys()))
logf.write("Total Number of Seq without hit: %i\n" % no_hit)
logf.write("Total Number of Seq with one orf having hit: %i\n" % single_orf)
logf.write("Total Number of Seq with multi orf having hit: %i\n" % multi_orf)
