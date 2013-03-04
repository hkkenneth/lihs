# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121122_gi_list_filter_taxonomy.py <GI LIST INPUT> <GI LIST OUTPUT>
# python ~/code/python/20121122_gi_list_filter_taxonomy.py gi_list gi_list_dhm
# [klui@compute-0-3 db]$ cut -f 2 -d ' ' gi_list_dhm | sort | uniq -c
# 255265 10090
# 647560 9606
#  32099 9615

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121122_gi_list_filter_taxonomy.py to get usage'

tax_id_set = set(["9615", "10090", "9606"]) # dog, mouse, human

outf = open(sys.argv[2], 'w')
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split(" ")
	if tokens[1] in tax_id_set:
		outf.write(line)

outf.close()
