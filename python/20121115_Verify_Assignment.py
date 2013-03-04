# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 15-11-2012
## Usage: python ~/code/python/20121115_Full_List_To_ORF_Range_And_Seq_Len.py <INPUT> <ORIGINAL>
## in 00dog, python ~/code/python/20121115_Verify_Assignment.py FINAL_full_list ../ORIGINAL_DOG_ASSIGNMENT

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20121115_Verify_Assignment.py to get usage'

assign_dict = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split(" ")
	id = tokens[0][tokens[0].find(">")+1:]
	found = False
	for tk in tokens[1:]:
		if tk.find("gi") == 0:
			assign_dict[id] = tk
			found = True
			break
	if not found:
		print "ERROR"

count = 0
same_hit = 0
for line in open(sys.argv[1]):
	tokens = line[:-1].split("\t")
	seq_id = tokens[17]
	if seq_id in assign_dict:
		count += 1
		if tokens[2].split(" ")[0] == assign_dict[seq_id]:
			same_hit += 1
		else:
			print seq_id
print count
print same_hit
