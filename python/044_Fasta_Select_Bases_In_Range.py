# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 012-14-2013 
## Usage: python ~/code/python/044_Fasta_Select_Bases_In_Range.py <ID LIST> <IN LIST OUTPUT FASTA> <INPUT FASTA ...>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/044_Fasta_Select_Bases_In_Range.py to get usage'

from Bio import SeqIO

RECORD_BUFFER_SIZE = 100000

name_set = set([])
name_list = []
start_dict = {} 
end_dict = {} 
for line in open(sys.argv[1], 'r'):
	tokens = line[:-1].split("\t")
	id = tokens[0]
	if id not in name_set:
		name_set.add(id)
		name_list.append(id)
		# assume 1-based
		start_dict[id] = []
		end_dict[id] = []
	start_dict[id].append(int(tokens[1])-1)
	end_dict[id].append(int(tokens[2]))

f1 = open(sys.argv[2], 'w')

r_dict = {}

r_list = []
size = 0

for s in sys.argv[3:]:
	for record in SeqIO.parse(s, "fasta"):
		if record.id in name_set:
			r_dict[record.id] = []
			for i in range(len(start_dict[record.id])):
				start = start_dict[record.id][i]
				end = end_dict[record.id][i]
				r = record[start:end]
				r.id = "%s_%i-%i" % (r.id, start, end)
				r_dict[record.id].append(r)

for name in name_list:
	if name in r_dict:
		r_list.extend(r_dict[name])

SeqIO.write(r_list, f1, "fasta")
f1.close()
