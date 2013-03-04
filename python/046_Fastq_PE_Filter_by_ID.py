# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 20-02-2013
## Usage: python ~/code/python/046_Fastq_PE_Filter_by_ID.py <ID LIST> <IN LIST OUTPUT FASTQ> <OUT LIST OUTPUT FASTQ> <INPUT FASTQ> <READ ID SEPARATER (DEFAULT SPACE)>
## This is PE in the sense that it tries to parse the paired ID!!
## ID in the list are only the "common part" (e.g. no /1 , /2) of the IDs
## Take a fastq file, can split the sequences into 2 files according to whether the id exists in the list
## for the in list output fastq file, the order is the same as the id list
## if the output fastq is not needed, use "-"

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/019f_Fastq_PE_Remove_Duplicates_With_Stat.py to get usage'

def linesToFile(lines, f):
	for line in lines:
		f.write(line)

read_id_sep = " "
if len(sys.argv) > 5:
	read_id_sep = sys.argv[5]

id_dict = {}
id_list = []
for line in open(sys.argv[1], 'r'):
	id_list.append(line[:-1])
	id_dict[line[:-1]] = []

if sys.argv[2] == "-":
	f1 = None
else:
	f1 = open(sys.argv[2], 'w')

if sys.argv[3] == "-":
	f2 = None
else:
	f2 = open(sys.argv[3], 'w')


f1in = open(sys.argv[4], 'r')
f1lines = f1in.readlines()
i = 0

while i < len(f1lines):
	id = f1lines[i][1:f1lines[i].find(read_id_sep)]
	if id in id_dict:
		if f1 is not None:
			id_dict[id] = f1lines[i:(i+4)]
	elif f2 is not None:
		linesToFile(f1lines[i:(i+4)], f2)
	i += 4

if f1 is not None:
	for id in id_list:
		if id in id_dict:
			linesToFile(id_dict[id], f1)

if f1 is not None:
	f1.close()

if f2 is not None:
	f2.close()
