import json
from pprint import pprint
import re

with open('sat.train.json') as fq:
    datafq = json.load(fq)
with open('gold_logical_form_train.json') as fglf:
	datafglf = json.load(fglf)

# print(type(datafglf))
# print(type(datafq))
glf_id_list = []
l_questions_with_glf = []

for x in datafglf:
	glf_id_list.append(x['id'])

for x in datafq:
	for y in datafglf:
		if x['id'] == y['id']:
			x['logicalForm'] = y['logicalForm']
			l_questions_with_glf.append(x)


# print(len(glf_id_list))
# q_with_glf_output = json.dump(l_questions_with_glf, indent=4)

q_with_glf_output = json.dumps(l_questions_with_glf, indent = 4)

# print(len(l_questions_with_glf))
print(q_with_glf_output)
# print(datafglf)


