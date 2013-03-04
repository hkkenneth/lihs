# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20121207_Broad_Fasta_Transform.py <INPUT LOCUS TAG FILE> <INPUT FASTA> <OUTPUT FASTA>

import sys
import string
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20121207_Broad_Fasta_Transform.py to get usage'

gene_dict = {}
gene_id = ""
locus_tag = ""
note = ""
ready = False
note_continue = False
print_it = False
for line in open(sys.argv[1], 'r'):
	if line.startswith("                     /gene="):
		gene_id = line[:-1].split("=")[1]
	elif line.startswith("                     /locus_tag="):
		locus_tag = line.split('"')[1]
		ready = True
	elif line.startswith("                     /note=") and ready:
		if (line.find('"') == line.rfind('"')) and (line.find("[") < 0):
			note_continue = True
		else:
			print_it = True
		note = line[(line.find('"')+1):(line.find("["))]
	elif note_continue and ready:
		note = note + line[len("                     "):line.rfind("[")]
		if line.find('"') >= 0:
			note_continue = False
			print_it = True
	if print_it and ready:
		print_it = False
		ready = False
		gene_dict[gene_id] = [locus_tag.upper(), note.replace(" ", "_")]

outf = open(sys.argv[3], 'w')
for line in open(sys.argv[2], 'r'):
	if line.startswith(">"):
		tokens = line.split(" ")
		gene_id = tokens[3].split(":")[1]
		if gene_id in gene_dict:
			tokens[0] = tokens[0] + "_" + gene_dict[gene_id][0] + "_" + gene_dict[gene_id][1]
		outf.write(string.join(tokens, " "))
	else:
		outf.write(line)

outf.close()
