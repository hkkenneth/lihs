import sys

outf = open(sys.argv[1] + ".good_qual", 'w')
outf2 = open(sys.argv[1] + ".bad_qual", 'w')

for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	prot_len = float(tokens[3])
	posi = float(tokens[10])
	iden = float(tokens[9])
	align_len_minus_gaps = float(tokens[8]) - float(tokens[11])
	if (iden / prot_len < 0.5) or (posi / prot_len < 0.7) or (align_len_minus_gaps / prot_len < 0.9):
		outf2.write(line)
	else:
		outf.write(line)
