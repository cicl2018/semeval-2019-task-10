from udpipe_model import Model
import json

# returns parsed sentences in conllu format
def get_conllu_repr(model, question):
	sentences = model.tokenize(question)
	for s in sentences:
		model.tag(s)
		model.parse(s)
	conllu = model.write(sentences, "conllu")

	return conllu

# transforms conllu format into an array of analysed sentences; every sentence is represented as an array of words; every word is represented as a dictionary which contains: form, lemma, pos, head and relation
def conllu_repr_into_arr(conllu_repr):
	# get a array with separate analysis of every sentence
	analyses = conllu_repr.split('\n\n')
	analyses = analyses[:-1]

	arr_analyses = []
	# take an analysis of a sentence
	for analysis in analyses:
		# print(analysis)
		arr_analysis = []
		# treat every line of the analysis as a word and its features
		lines = analysis.split("\n")
		for line in lines:
			if not line.startswith("#") and line != "":
				dict_properties = {}
				properties = line.split("\t")
				
				dict_properties["form"] = properties[1]
				dict_properties["lemma"] = properties[2]
				dict_properties["pos"] = properties[3]
				dict_properties["grammar"] = properties[5]
				dict_properties["head"] = int(properties[6])
				dict_properties["relation"] = properties[7]

				arr_analysis.append(dict_properties)

		arr_analyses.append(arr_analysis)

	return arr_analyses

# finds verb associated with the quantity or returns None when there is no sich verb
def find_verb(analysis, head_index):
	if head_index != 0:
		candidate = analysis[head_index-1]

		if candidate["pos"] != "VERB":
			new_head_index = candidate["head"]
			return find_verb(analysis, new_head_index)
		else:
			return candidate
	else:
		return None

# finds noun which is subject of the associated verb
def find_noun(analysis, verb):
	if verb != None:
		verb_index = analysis.index(verb) + 1
		for word in analysis:
			# NOUN!!!
			if word["head"] == verb_index and word["relation"].startswith("nsubj"):
				return word
		return None
	return None

# finds unit of quantity and construction "of + N", if there is one following the unit
def find_unit(analysis, i):
	head_index = analysis[i]["head"]

	unit = None
	# extract unit
	candidate = analysis[head_index-1]
	if candidate["pos"] != "NUM":
		unit = candidate["lemma"]

	# check if there is a word "of" after the unit; if there is, extract "of + N"
	next_word = analysis[head_index]
	if next_word["form"] == "of":

		head_index_of = next_word["head"]
		candidate_of = analysis[head_index_of-1]
		if candidate_of["pos"] == "NOUN":
			unit += " of " + analysis[head_index_of-1]["lemma"]

	return unit

# finds nouns related to the unit (in PP connected to the unit)
def find_nouns(analysis, next_word_index):
	nouns = []

	next_word = analysis[next_word_index]
	if next_word["pos"] == "ADP":
		if next_word["lemma"] != "of" and next_word["lemma"] != "per":
			if analysis[next_word_index+1]["lemma"] != "each":
				head_index_prep = next_word["head"]
				candidate = analysis[head_index_prep-1]
				if candidate["pos"] == "NOUN":
					noun = candidate["lemma"]
					nouns.append(noun)

					nouns += find_nouns(analysis, head_index_prep)

	return nouns

# finds second part of unit if quantity has a rate
def find_rate(analysis, next_word_index, verb, subj):
	next_word = analysis[next_word_index]
	# "per"/"a"/"every" + noun
	if next_word["lemma"] == "per" or next_word["lemma"] == "a":
		head_index = next_word["head"]-1
		return analysis[head_index]["lemma"]
	# "each"
	if next_word["lemma"] == "each":
		head_index = next_word["head"]-1
		# "each" + noun
		if head_index > next_word_index:
			return analysis[head_index]["lemma"]
		# "each" is connected to subject or object
		if verb != None:
			verb_index = analysis.index(verb)+1
			# if there is an object different from unit, "each" is connected to object
			for word in analysis:
				if word["head"] == verb_index and word["relation"] == "obj":
					unit_index = next_word_index - 1
					if word != analysis[unit_index]:
						return word["lemma"]
		# if there is no such object, "each" is connected to subject
		if subj != None:
			return subj["lemma"]
	# preposition + "each" + noun
	if next_word["pos"] == "ADP":
		next_next_word = analysis[next_word_index+1]
		if next_next_word["lemma"] == "each":
			head_index = next_next_word["head"]-1
			return analysis[head_index]["lemma"]
	# "each" + subject
	if subj != None:
		subj_index = analysis.index(subj)+1
		index = 0
		for index in range(0, subj_index):
			word = analysis[index]
			if word["head"] == subj_index and word["lemma"] == "each":
				return subj["lemma"]

# extracts adverbs and comparative adjectives in a window of size 5 around the quantity
def find_adverbs(analysis, i):
	adverbs = ""

	low_border = i - 5
	if low_border < 0:
		low_border = 0
	for index in range(low_border, i):
		word = analysis[index]
		if word["pos"] == "ADV":
			adverbs += word["lemma"] + " "
		elif word["pos"] == "ADJ" and word["grammar"] == "Degree=Cmp":
			adverbs += word["lemma"] + " "

	high_border = i + 5
	if high_border > len(analysis):
		high_border = len(analysis)
	for index in range(i, high_border):
		word = analysis[index]
		if word["pos"] == "ADV":
			adverbs += word["lemma"] + " "
		elif word["pos"] == "ADJ" and word["grammar"] == "Degree=Cmp":
			adverbs += word["lemma"] + " "

	return adverbs.strip()

# looks for quantity in part of sentence after border; represents quantity as dictionary with quantity itself, its associated verb (lemma), subject of associated verb (lemma), unit, nouns connected to unit as PPs, rate (2nd part of unit), if quantity has rate
def extract_features(quantity, analysis, border, new_quantities, last_sent_tokens):
	for i in range(border, len(analysis)):
		if analysis[i]["form"] == quantity:
			new_quantity = {}
			new_quantity["value"] = quantity

			verb = find_verb(analysis, i)
			new_quantity["verb"] = verb["lemma"] if verb != None else None

			subj = find_noun(analysis, verb)
			new_quantity["subj"] = subj["lemma"] if subj != None else None

			unit = find_unit(analysis, i)
			new_quantity["unit"] = unit

			score = 0
			if unit != None:
				units = unit.split(" ")
				for un in units:
					if un in last_sent_tokens:
						score += 1
			new_quantity["if_unit_in_q"] = score

			nouns = find_nouns(analysis, analysis[i]["head"])

			score = 0
			if nouns != []:
				new_quantity["nouns"] = nouns
				for noun in nouns:
					if noun in last_sent_tokens:
						score += 1
			else:
				new_quantity["nouns"] = None
			new_quantity["noun_in_q"] = score

			if i+1 > analysis[i]["head"]:
				rate = find_rate(analysis, i+1, verb, subj)
			else:
				rate = find_rate(analysis, analysis[i]["head"], verb, subj)
			if rate != None:
				new_quantity["rate"] = rate
				new_quantity["if_rate"] = True
				if rate in last_sent_tokens or unit in last_sent_tokens:
					new_quantity["if_rate_in_q"] = True
				else:
					new_quantity["if_rate_in_q"] = False
			else:
				new_quantity["rate"] = None
				new_quantity["if_rate"] = False
				new_quantity["if_rate_in_q"] = None

			adverbs = find_adverbs(analysis, i)
			new_quantity["adverbs"] = adverbs if adverbs != "" else None

			new_quantities.append(new_quantity)
			return i
	return len(analysis)

def extract_features_for_all(quantities, analyses, last_sent_tokens):
	new_quantities = []

	found = 0
	for analysis in analyses:
		border = -1
		for i in range(found, len(quantities)):
			border = extract_features(quantities[i], analysis, border+1, new_quantities, last_sent_tokens)
		found = len(new_quantities)

	max_unit = 0
	max_noun = 0
	max_both = 0
	for quantity in new_quantities:
		if_unit_in_q = quantity["if_unit_in_q"]
		noun_in_q = quantity["noun_in_q"]
		if if_unit_in_q > max_unit:
			max_unit = quantity["if_unit_in_q"]
		if noun_in_q > max_noun:
			max_noun = quantity["noun_in_q"]
		if if_unit_in_q + noun_in_q > max_both:
			max_both = if_unit_in_q + noun_in_q

	ultra_new_quantities = []
	num_max_matches = 0
	for quantity in new_quantities:
		new_quantity = dict(quantity)
		new_quantity["other_unit_matches_better"] = True if quantity["if_unit_in_q"] < max_unit else False
		new_quantity["other_noun_matches_better"] = True if quantity["noun_in_q"] < max_noun else False
		ultra_new_quantities.append(new_quantity)

		if quantity["if_unit_in_q"] + quantity["noun_in_q"] == max_both:
			num_max_matches += 1

	return ultra_new_quantities, num_max_matches

def run_on_all_questions(filename):
	model = Model('/Users/alinabaranova/udpipe-ud-2.3-181115/english-ewt-ud-2.3-181115.udpipe')
	with open(filename) as file:
		questions = json.load(file)

	new_questions = []

	for question in questions:
		text = question['question_mod']

		conllu_repr = get_conllu_repr(model, text)
		arr_analyses = conllu_repr_into_arr(conllu_repr)

		# question tokens
		last_sent = arr_analyses[-1]
		last_sent_tokens = []
		for word in last_sent:
			last_sent_tokens.append(word["lemma"])

		# whether question mentions comparison-related tokens ("more", "less", "than")
		if "more" in last_sent_tokens or "less" in last_sent_tokens or "than" in last_sent_tokens:
			q_comp_tokens = True
		else:
			q_comp_tokens = False

		# whether question asks for rate ("each", "one")
		if "each" in last_sent_tokens or "one" in last_sent_tokens:
			q_rate = True
		else:
			q_rate = False

		quantities = []
		for quantity in question['quantities']:
			quantities.append(quantity['value'])

		print(len(quantities))

		new_quantities, num_max_matches = extract_features_for_all(quantities, arr_analyses, last_sent_tokens)

		print(len(new_quantities))
		print('\n')

		new_question = dict(question)
		new_question['quantities'] = new_quantities
		new_question['q_comp_tokens'] = q_comp_tokens
		new_question['q_rate'] = q_rate
		new_question['num_max_matches'] = num_max_matches

		new_questions.append(new_question)
		# print(conllu_repr)

	return new_questions

new_questions = run_on_all_questions('./files/open.train_answered_with-reverse.json')
with open('./files/open.train_answered_with-reverse_features.json', 'w') as file:
	json.dump(new_questions, file, indent=4)

# new_questions = run_on_all_questions('./files/open.train_answered.json')
# with open('./files/open.train_answered_features.json', 'w') as file:
# 	json.dump(new_questions, file, indent=4)

# new_questions = run_on_all_questions('open_modified.json')
# with open('open_modified_features.json', 'w') as file:
	# json.dump(new_questions, file, indent=4)

# question = "Mary took 30 minutes to drive a certain distance at 60 miles per hour. How many minutes did John take, driving at 20 miles per hour, to go the same distance?"
# quantities = ["30", "60", "20"]

# model = Model('/Users/alinabaranova/udpipe-ud-2.3-181115/english-ewt-ud-2.3-181115.udpipe')
# conllu_repr = get_conllu_repr(model, question)
# # print(conllu_repr)
# arr_analyses = conllu_repr_into_arr(conllu_repr)

# last_sent = arr_analyses[-1]
# last_sent_tokens = []
# for word in last_sent:
# 	last_sent_tokens.append(word["lemma"])
# print(last_sent_tokens)

# if "more" in last_sent_tokens or "less" in last_sent_tokens or "than" in last_sent_tokens:
# 	q_comp_tokens = True
# else:
# 	q_comp_tokens = False

# if "each" in last_sent_tokens or "one" in last_sent_tokens:
# 	q_rate = True
# else:
# 	q_rate = False

# new_quantities = extract_features_for_all(quantities, arr_analyses, last_sent_tokens)
# for quantity in new_quantities:
# 	print(quantity)
