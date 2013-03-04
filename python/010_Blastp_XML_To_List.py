# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/010_Blastp_XML_To_List.py <XML> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/010_Blastp_XML_To_List.py to get usage'

from Bio import SeqIO
from Bio.Blast import NCBIXML

query_count = 0
query_with_hit_count = 0
hit_count = 0
hit_protein_set = set([])
line_count = 0
logf = open(sys.argv[2] + ".py010.log" , 'w')
outf = open(sys.argv[2] + ".py010.out" , 'w')
for record in NCBIXML.parse(open(sys.argv[1], 'r')):
	query_count += 1
	if len(record.alignments) > 0:
		query_with_hit_count += 1
	else:
		continue
	str_query = "%s\t%i\t" % (record.query.split(" ")[0], record.query_length)
	for al_i in range(len(record.alignments)):
		al = record.alignments[al_i]
		de = record.descriptions[al_i]
		str_hit = "%s %s\t%i\t%i\t%s\t" % (al.hit_id, al.hit_def, al.length, len(al.hsps), str(de.e))
		#str_hit = "%s\t%i\t%i\t%s\t" % (al.hit_def, al.length, len(al.hsps), str(de.e))
		hit_protein_set.add(al.hit_def.split(" ")[0])
		hit_count += 1
		for hsp in al.hsps:
			str_hsp = "%i-%i\t%i-%i\t%i\t%i\t%i\t%i\t%s\t%s\t%s\t%s\t" % (hsp.query_start, hsp.query_end, hsp.sbjct_start, hsp.sbjct_end, hsp.align_length, hsp.identities, hsp.positives, hsp.gaps, hsp.expect, hsp.query, hsp.match, hsp.sbjct)
			line_count += 1
			outf.write("%s%s%s%i\n" % (str_query, str_hit, str_hsp, line_count))
			
logf.write("Input XML file: %s\n" % sys.argv[1])
logf.write("\nQuery count: %i\n" % query_count)
logf.write("Query with hit count: %i\n" % query_with_hit_count)
logf.write("Query with no hit count: %i\n" % (query_count - query_with_hit_count))
logf.write("\nHit count: %i\n" % hit_count)
logf.write("Unique Hit count: %i\n" % len(hit_protein_set))
logf.write("\nHSP count: %i\n" % line_count)
logf.close()
