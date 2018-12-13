import json

with open('sat.train.json') as fq:
    datafq = json.load(fq)
with open('gold_logical_form_train.json') as fglf:
	datafglf = json.load(fglf)

l_questions_with_glf = []

for x in datafq:
	for y in datafglf:
		if x['id'] == y['id']:
			x['logicalForm'] = y['logicalForm']
			l_questions_with_glf.append(x)

q_with_glf_output = json.dumps(l_questions_with_glf, indent = 4)

with open('questions_with_glf.json', 'w+') as f:
	f.write(q_with_glf_output)