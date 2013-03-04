# Author: Kenneth Lui <hkkenneth@gmail.com>
# Last Updated on: 
## Usage: python ~/code/python/20130125_Ferret_Blastn_Check.py <PY 010 LIST> <CK Gene Symbol Assignment> <OUTPUT PREFIX>

import sys
if len(sys.argv) < 4:
        raise SystemExit, 'use grep "##" ~/code/python/20130125_Ferret_Blastn_Check.py to get usage'

singlef = open(sys.argv[3] + ".py20130125.single", 'w')
samef = open(sys.argv[3] + ".py20130125.same_gs", 'w')
difff = open(sys.argv[3] + ".py20130125.diff_gs", 'w')


gs_dict = {}
for line in open(sys.argv[2], 'r'):
	tokens = line[:-1].split("\t")
	if tokens[0] in gs_dict:
		gs_dict[tokens[0]] = gs_dict[tokens[0]] + "/" + tokens[1].upper()
	else:
		gs_dict[tokens[0]] = tokens[1].upper()

line_dict = {}
for line in open(sys.argv[1], 'r'):
	tokens = line.split("\t")
	if tokens[2].find("ref|") < 0:
		continue
	if tokens[0] in line_dict:
		line_dict[tokens[0]].append(line)
	else:
		line_dict[tokens[0]] = [line]



for k in line_dict.keys():
	type = 1
	assigned_gs = "NOT_ASSIGNED"
	if k in gs_dict:
		assigned_gs = gs_dict[k]
	if len(line_dict[k]) > 1:
		type = 2
		for line in line_dict[k]:
			tokens = line.split("\t")
			gs = "GS_NOT_FOUND"
			i = tokens[2].rfind(")")
			if i >= 0:
				before_par = tokens[2][:tokens[2].rfind(")")]
				i = before_par.rfind("(")
				if i >= 0:
					gs = before_par[i+1:]
			if gs != assigned_gs:
				type = 3
	for line in line_dict[k]:
		tokens = line.split("\t")
		gs = "GS_NOT_FOUND"
		i = tokens[2].rfind(")")
		if i >= 0:
			before_par = tokens[2][:tokens[2].rfind(")")]
			i = before_par.rfind("(")
			if i >= 0:
				gs = before_par[i+1:]
		if type == 1:
			singlef.write("%s\t%s\t%s\n" % (line[:-1], assigned_gs, gs))
		elif type == 2:
			samef.write("%s\t%s\t%s\n" % (line[:-1], assigned_gs, gs))
		elif type == 3:
			difff.write("%s\t%s\t%s\n" % (line[:-1], assigned_gs, gs))

singlef.close()
samef.close()
difff.close()
