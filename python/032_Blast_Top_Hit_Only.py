# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/032_Blast_Top_Hit_Only.py <XML> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/032_Blast_Top_Hit_Only.py to get usage'

from Bio import SeqIO
from Bio.Blast import NCBIXML

query_count = 0
query_with_hit_count = 0
hit_count = 0
hit_protein_set = set([])
line_count = 0
outf = open(sys.argv[2] + ".py032.out" , 'w')
for record in NCBIXML.parse(open(sys.argv[1], 'r')):
	query_count += 1
	line_count += 1
	str_query = "%s\t%i\t" % (record.query.split(" ")[0], record.query_length)
	if len(record.alignments) > 0:
		query_with_hit_count += 1
	else:
		outf.write("%s_NO_HIT_\n" % str_query)
		continue
	for al_i in range(len(record.alignments)):
		al = record.alignments[al_i]
		de = record.descriptions[al_i]
		str_hit = "%s %s\t%i\t%i\t" % (al.hit_id, al.hit_def, al.length, len(al.hsps))
		hsp = al.hsps[0]
		str_hsp = "%i\t%i\t" % (hsp.align_length, hsp.identities)
		str_query = str_query + str_hit + str_hsp
	outf.write(str_query + "\n")
	
outf.close()	
