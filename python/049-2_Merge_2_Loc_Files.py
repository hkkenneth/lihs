# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/049-2_Merge_2_Loc_Files.py <READ 1 IN> <READ 2 IN> <OUTPUT PREFIX> <SEQ ID SEPARATOR>
## wc -l <OUTPUT PREFIX>.py049-2*
## sort -k 5 -n -r -t $'\t' <OUTPUT PREFIX>.py049-2.stat | grep "MIDDLE" | head
## sort -k 5 -n -r -t $'\t' <OUTPUT PREFIX>.py049-2.stat 

import sys
if len(sys.argv) < 5:
        raise SystemExit, 'use grep "##" ~/code/python/049-2_Merge_2_Loc_Files.py to get usage'

read_id_sep = sys.argv[4]

read_dict = {}
for s in sys.argv[1:3]:
	for line in open(s, 'r'):
		tokens = line.split("\t")
		read_id = tokens[0].split(read_id_sep)[0]
		if read_id not in read_dict:
			read_dict[read_id] = []
		read_dict[read_id].append(line)

outf1 = open(sys.argv[3] + ".py049-2.single" , 'w')
outf2 = open(sys.argv[3] + ".py049-2.pair" , 'w')
outf3 = open(sys.argv[3] + ".py049-2.pair.stat" , 'w')
outf4 = open(sys.argv[3] + ".py049-2.single.stat" , 'w')

# to find "ends" stat
outf5 = open(sys.argv[3] + ".py049-2.end.stat" , 'w')
logf = open(sys.argv[3] + ".py049-2.log" , 'w')

connect_dict = {}
single_dict = {}
merge_dict = {}	# for outf5

for id in read_dict.keys():
	if len(read_dict[id]) == 1:
		for line in read_dict[id]:
			outf1.write(line)
		tokens1 = read_dict[id][0][:-1].split("\t")
		str1 = tokens1[1] + "\t" + tokens1[2] + "\t\t"
		if str1 in single_dict:
			single_dict[str1] += 1
			merge_dict[str1] += 1
		else:
			single_dict[str1] = 1
			merge_dict[str1] = 1
	else:
		tokens1 = read_dict[id][0][:-1].split("\t")
		tokens2 = read_dict[id][1][:-1].split("\t")
		# seq1 loc1 seq2 loc2 pos1 pos2
		outf2.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (id, tokens1[1], tokens1[2], tokens2[1], tokens2[2], tokens1[3], tokens2[3]))
		# seq1 loc1 seq2 loc2
		str1 = tokens1[1] + "\t" + tokens1[2] + "\t" + tokens2[1] + "\t" + tokens2[2]
		if str1 in connect_dict:
			connect_dict[str1] += 1
		else:
			connect_dict[str1] = 1
		if tokens1[1] > tokens2[1]:
			str2 = tokens1[1] + "\t" + tokens1[2] + "\t" + tokens2[1] + "\t" + tokens2[2]
		else:
			str2 = tokens2[1] + "\t" + tokens2[2] + "\t" + tokens1[1] + "\t" + tokens1[2]
		if str2 in merge_dict:
			merge_dict[str2] += 1
		else:
			merge_dict[str2] = 1


sorted_keys = connect_dict.keys()
sorted_keys.sort()
for k in sorted_keys:
	outf3.write("%s\t%i\n" % (k, connect_dict[k]))
outf3.close()
		
sorted_keys = single_dict.keys()
sorted_keys.sort()
for k in sorted_keys:
	outf4.write("%s\t%i\n" % (k, single_dict[k]))
outf4.close()

sorted_keys = merge_dict.keys()
sorted_keys.sort()
l_dict = {}
r_dict = {}

for k in sorted_keys:
	if k.find("MIDDLE") >= 0:
		continue
	outf5.write("%s\t%i\n" % (k, merge_dict[k]))
	tokens = k.split("\t")
	if tokens[1] == "L_END":
		if tokens[0] not in l_dict:
			l_dict[tokens[0]] = []
		if tokens[2] != "":
			l_dict[tokens[0]].append(k)
	elif tokens[1] == "R_END":
		if tokens[0] not in r_dict:
			r_dict[tokens[0]] = []
		if tokens[2] != "":
			r_dict[tokens[0]].append(k)
outf5.close()

logf.write("Number of Contigs with a reads cluster at left end:\t%i\n" % len(l_dict))
count = 0
count2 = 0
for k in l_dict.keys():
	if len(l_dict[k]) == 1:
		count += 1
	elif len(l_dict[k]) > 1:
		count2 += 1
logf.write("Number of Contigs with a unique scaffold-able left end:\t%i\n" % count)
logf.write("Number of Contigs with an ambiguous scaffold-able left end:\t%i\n" % count2)

logf.write("Number of Contigs with a reads cluster at right end:\t%i\n" % len(r_dict))
count = 0
count2 = 0
for k in r_dict.keys():
	if len(r_dict[k]) == 1:
		count += 1
	elif len(r_dict[k]) > 1:
		count2 += 1
logf.write("Number of Contigs with a unique scaffold-able right end:\t%i\n" % count)
logf.write("Number of Contigs with an ambiguous scaffold-able right end:\t%i\n" % count2)

logf.write("Number of Contigs with a reads cluster at both end:\t%i\n" % len(set(l_dict.keys()) & set(r_dict.keys())))
logf.close()
