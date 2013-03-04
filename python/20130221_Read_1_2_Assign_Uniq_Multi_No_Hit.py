# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 21-02-2013 
## Usage: python ~/code/python/20130221_Read_1_2_Assign_Uniq_Multi_No_Hit.py <PAIR END FASTQ 1> <PAIR END FASTQ 2> <BOWTIE OUT 1> <BOWTIE OUT 2> <ID SEP> <OUTPUT PREFIX>


import sys
if len(sys.argv) < 7:
        raise SystemExit, 'use grep "##" ~/code/python/20130221_Read_1_2_Assign_Uniq_Multi_No_Hit.py to get usage'

id_sep = sys.argv[5]
the_dict = {}
logf = open(sys.argv[6] + ".py0221.log", 'w')
outf = open(sys.argv[6] + ".py0221.out", 'w')
logf.write("Parameters:\n")
logf.write("Fastq 1:\t%s\n" % sys.argv[1])
logf.write("Fastq 2:\t%s\n" % sys.argv[2])
logf.write("Bowtie 1:\t%s\n" % sys.argv[3])
logf.write("Bowtie 2:\t%s\n" % sys.argv[4])
logf.write("ID sep:\t%s\n" % sys.argv[5])

r1 = sys.argv[1]
r2 = sys.argv[2]
for s in sys.argv[1:3]:
	the_dict[s] = {}
	line_count = 0
	for line in open(s, 'r'):
		if line_count % 4 == 0:
			id = line[1:].split(id_sep)[0]
			the_dict[s][id] = 0
		line_count += 1
	logf.write("Number of reads in %s:\t%i\n" % (s, line_count/4))
	logf.write("Number of unique read IDs in %s:\t%i\n" % (s, len(the_dict[s].keys())))

# Should be zeroes!
logf.write("Number of read IDs in %s only:\t%i\n" % (r1, len(set(the_dict[r1].keys()) - set(the_dict[r2].keys()))))
logf.write("Number of read IDs in %s only:\t%i\n" % (r2, len(set(the_dict[r2].keys()) - set(the_dict[r1].keys()))))

def add_to_the_dict(bowtie_f, dict):
	not_found_count = 0
	for line in open(bowtie_f, 'r'):
		r_id = line.split(id_sep)[0]
		if r_id in dict:
			dict[r_id] += 1
		else:
			not_found_count += 1
	return not_found_count
		
not_found_count1 = add_to_the_dict(sys.argv[3], the_dict[r1])
not_found_count2 = add_to_the_dict(sys.argv[4], the_dict[r2])

logf.write("Number of alignment in %s which is not in %s:\t%i\n" % (sys.argv[3], sys.argv[1], not_found_count1))
logf.write("Number of alignment in %s which is not in %s:\t%i\n" % (sys.argv[4], sys.argv[2], not_found_count2))

union_id = set(the_dict[r1].keys()) | set(the_dict[r2].keys())

logf.write("Number of IDs in either fastq:\t%i\n" % (len(union_id)))

flag_dict = {120:0, 220:0, 320:0, 110:0, 210:0, 310:0, 130:0, 230:0, 330:0 }

for id in union_id:
	outf.write("%s" % id)
	flag = 0
	for s in sys.argv[1:3]:
		status="NO_READ"
		if id in the_dict[s]:
			if the_dict[s][id] == 0:
				status="NO_HIT"
				flag += 1
			elif the_dict[s][id] == 1:
				status="UNIQUE(1)"
				flag += 2
			else:
				status="MULTI(%i)" % the_dict[s][id]
				flag += 3
		flag = flag * 10
		outf.write("\t%s" % status)
		if flag in flag_dict:
			flag_dict[flag] += 1
	outf.write("\n")
logf.write("read 2 uniq, read 1 uniq:\t%i\n" % flag_dict[220])
logf.write("read 2 uniq, read 1 multi:\t%i\n" % flag_dict[320])
logf.write("read 2 uniq, read 1 no:\t%i\n" % flag_dict[120])

logf.write("read 2 multi, read 1 uniq:\t%i\n" % flag_dict[230])
logf.write("read 2 multi, read 1 multi:\t%i\n" % flag_dict[330])
logf.write("read 2 multi, read 1 no:\t%i\n" % flag_dict[130])

logf.write("read 2 no, read 1 uniq:\t%i\n" % flag_dict[210])
logf.write("read 2 no, read 1 multi:\t%i\n" % flag_dict[310])
logf.write("read 2 no, read 1 no:\t%i\n" % flag_dict[110])
outf.close()
logf.close()
