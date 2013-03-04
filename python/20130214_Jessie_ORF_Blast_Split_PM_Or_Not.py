# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20130214_Jessie_ORF_Blast_Split_PM_Or_Not.py <INPUT> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 3:
        raise SystemExit, 'use grep "##" ~/code/python/20130214_Jessie_ORF_Blast_Split_PM_Or_Not.py to get usage'

orf_list = []
orf_dict = {}
pm_line = []
non_pm_line = []
align_dict = {}
iden_dict = {}
outf = open(sys.argv[2] + ".py20130214.out", 'w')
for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	if tokens[0] not in orf_dict:
		orf_dict[tokens[0]] = tokens[1]
		orf_list.append(tokens[0])
		align_dict[tokens[0]] = {}
		iden_dict[tokens[0]] = {}
	if tokens[2] not in align_dict[tokens[0]]:
		align_dict[tokens[0]][tokens[2]] = 0
		iden_dict[tokens[0]][tokens[2]] = 0
	align_dict[tokens[0]][tokens[2]] += int(tokens[8]) 
	iden_dict[tokens[0]][tokens[2]] += int(tokens[9])

	if "Penicillium marneffei" in tokens[2]:
		pm_line.append(line)
	else:
		non_pm_line.append(line)

for id in orf_list:
	outf.write("%s\t%s\t" % (id, orf_dict[id]))
	best_non_pm_id = "NO_HIT"
	best_non_pm_per = 0.0
	best_pm_id = "NO_HIT"
	best_pm_per = 0.0
	non_hypo_non_pm_id = "NO_HIT"
	non_hypo_non_pm_per = 0.0
	non_hypo_pm_id = "NO_HIT"
	non_hypo_pm_per = 0.0

	for prot in align_dict[id]:
		percent = float(iden_dict[id][prot]) / float(align_dict[id][prot])
		if "Penicillium marneffei" in prot:
			if percent > best_pm_per:
				best_pm_per = percent
				best_pm_id = prot
			if "hypothetical" not in prot:
				if percent > non_hypo_pm_per:
					non_hypo_pm_per = percent
					non_hypo_pm_id = prot
		else:
			if percent > best_non_pm_per:
				best_non_pm_per = percent
				best_non_pm_id = prot
			if "hypothetical" not in prot:
				if percent > non_hypo_non_pm_per:
					non_hypo_non_pm_per = percent
					non_hypo_non_pm_id = prot

	outf.write("%s\t%s\t" % (best_pm_id, str(best_pm_per)))
	outf.write("%s\t%s\t" % (non_hypo_pm_id, str(non_hypo_pm_per)))
	outf.write("%s\t%s\t" % (best_non_pm_id, str(best_non_pm_per)))
	outf.write("%s\t%s\t" % (non_hypo_non_pm_id, str(non_hypo_non_pm_per)))
	outf.write("\n")

outf.close()
