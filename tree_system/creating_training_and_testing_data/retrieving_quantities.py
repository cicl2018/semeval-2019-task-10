from latex_transformer import latex_to_decimal
import re
import json

def preprocessing_answer(answer):
	begin_of_re = '(?:(?<=\\s)|(?<=^))'
	end_of_re = '(?=(?:(!|\\(|\\)|:|;|"|\'|,|\\.|\\?|\\s|$)))'

	#regular expressions for:
	# deleting , in numbers (e.g. 96,000)
	re_com = re.compile('(?<=[0-9]),(?=[0-9])')
	# latex expressions
	re_la = re.compile(begin_of_re + '(\\\\\\((.+?)\\\\\\))' + end_of_re)

	# array for changing all the numbers written with words into numerical forms
	words_to_numbers = {'(o|O)ne': '1', '(t|T)wo': '2', '(t|T)hree': '3', '(f|F)our': '4', '(f|F)ive': '5', '(s|S)ix': '6', '(s|S)even': '7', '(e|E)ight': '8', '(n|N)ine': '9', '(t|T)en': '10', '(e|E)leven': '11', '(t|T)welve': '12', '(d|D)ozen': '12', '(t|T)hirteen': '13', '(f|F)ourteen': '14', '(s|S)ixteen': '16', '(s|S)eventeen': '17', '(e|E)ighteen': '18', '(n|N)ineteen': '19', '(t|T)wenty': '20', '(t|T)hirty': '30', '(f|F)ourty': '40', '(f|F)ifty': '50', '(s|S)ixty': '60', '(s|S)eventy': '70', '(e|E)ighty': '80', '(n|N)inety': '90'}

	# change all the numbers written with words into numerical forms
	for word in words_to_numbers:
		answer = re.sub(begin_of_re + word + end_of_re, words_to_numbers[word], answer)

	# delete , from numbers
	answer = re_com.sub('', answer)
	# delete "\\$"
	answer = answer.replace('\\$', '')
	# delete "\\%"
	answer = answer.replace('\\%', '')

	n = re_la.findall(answer)
	if n != ():
		for tup in n:
			number = latex_to_decimal(tup[1])
			if number != None:
				answer = answer.replace(tup[0], number)

	return answer

def extract_from_answer(answer):
	m = re.match('\\\\\\(.+?(\\\\\\))', answer)
	if m == None:
		begin_of_re = '(?:(?<=\\s)|(?<=^))'
		end_of_re = '(?:(?=!|\\(|\\)|;|"|\'|,|\\.|\\?|\\s|:\\s|$))'

		#regular expressions for extracting:
		# numbers with "."
		re_dot = '[0-9]+\\.[0-9]+'
		# normal numbers
		re_nor = '[0-9]+'
		# number-unit (e.g. 13-inch)
		re_nu = '(' + re_dot + '|' + re_nor + ')\\-[a-zA-Z]+'
		# time
		re_ti = '([0-9]{1,2}:[0-9]{2})'

		# final regex - a combination of all regexes
		final_re = re.compile(begin_of_re + '(?:' + re_nu + '|(\\-?' + re_dot + ')|(\\-?' + re_nor + ')|' + re_ti + ')' + end_of_re)

		# array for extracted quantities
		quantities = []

		# write every quantity to the array
		n = final_re.findall(answer)
		if n != ():
			for tup in n:
				for i in range(len(tup)):
					if tup[i] != '':
						quantities.append(tup[i])

		return quantities
	return []

def preprocessing_questions(arr):
	new_arr = []

	begin_of_re = '(?:(?<=\\s)|(?<=^))'
	end_of_re = '(?:(?=!|\\(|\\)|:|;|"|\'|,|\\.|\\?|\\s))'

	#regular expressions for:
	# deleting the parentheses in the end of the problem
	re_par = re.compile('\\(.+?(\\)\\.?$)')
	# replacing "once" by "1 time", "twice" - by "2 times"
	re_once = re.compile('(?<=[^(at)])\\sonce' + end_of_re)
	re_twice = re.compile(begin_of_re + 'twice' + end_of_re)
	# deleting (1), (2) etc.
	re_num = re.compile('\\s\\([0-9]+\\)' + end_of_re)
	# deleting , in numbers (e.g. 96,000)
	re_com = re.compile('(?<=[0-9]),(?=[0-9])')
	# replacing "half an hour", "quarter-mile", "quarter-hour" by "0.5-hour", "0.25-mile" and "0.25-hour" accordingly
	re_h1 = re.compile(begin_of_re + '((h|H)alf an hour|(h|H)alf-hour)' + end_of_re)
	re_h2 = re.compile(begin_of_re + '(q|Q)uarter-hour' + end_of_re)
	re_m = re.compile(begin_of_re + '(q|Q)uarter-mile' + end_of_re)
	# replacing "half", "one-half" by "0.5"
	re_half = re.compile(begin_of_re + '((o|O)ne-half|(h|H)alf)' + end_of_re)
	# latex expressions
	re_la = re.compile(begin_of_re + '(\\\\\\((.+?)\\\\\\))' + end_of_re)

	# numbers with "."
	re_dot = '[0-9]+\\.[0-9]+'
	# normal numbers
	re_nor = '[0-9]+'
	# numbers with "$" sign
	re_dol = re.compile(begin_of_re + '(\\\\\\()?\\\\\\$' + '(' + re_dot + '|' + re_nor + ')(\\\\\\))?' + end_of_re)
	# numbers with "%" sign
	re_per = re.compile(begin_of_re + '(\\\\\\()?(' + re_dot + '|' + re_nor + ')\\\\%(\\\\\\))?' + end_of_re)
	# variables in construction like "\\(f\\)"
	re_var = re.compile(begin_of_re + '\\\\\\(([b-z])\\\\\\)' + end_of_re)

	# array for changing all the numbers written with words into numerical forms
	words_to_numbers = {'(o|O)ne': '1', '(t|T)wo': '2', '(t|T)hree': '3', '(f|F)our': '4', '(f|F)ive': '5', '(s|S)ix': '6', '(s|S)even': '7', '(e|E)ight': '8', '(n|N)ine': '9', '(t|T)en': '10', '(e|E)leven': '11', '(t|T)welve': '12', '(d|D)ozen': '12', '(t|T)hirteen': '13', '(f|F)ourteen': '14', '(s|S)ixteen': '16', '(s|S)eventeen': '17', '(e|E)ighteen': '18', '(n|N)ineteen': '19', '(t|T)wenty': '20', '(t|T)hirty': '30', '(f|F)ourty': '40', '(f|F)ifty': '50', '(s|S)ixty': '60', '(s|S)eventy': '70', '(e|E)ighty': '80', '(n|N)inety': '90'}

	for element in arr:
		line = element['question']
		# line = element
		new_element = {}

		# delete (1), (2) etc.
		line = re_num.sub('', line)

		# delete the parentheses in the end of the problem
		line = re_par.sub('', line)

		# replace "once" by "1 time", "twice" - by "2 times"
		line = re_once.sub(' 1 time', line)
		line = re_twice.sub('2 times', line)

		# replace "half an hour"/"half-hour", "quarter-mile", "quarter-hour" by "0.5-hour", "0.25-mile" and "0.25-hour" accordingly
		line = re_h1.sub('0.5-hour', line)
		line = re_h2.sub('0.25-hour', line)
		line = re_m.sub('0.25-mile', line)

		# replace "half", "one-half" by "0.5"
		line = re_half.sub('0.5', line)

		# change all the numbers written with words into numerical forms
		for word in words_to_numbers:
			line = re.sub(begin_of_re + word + '(?=' + end_of_re + '|\\-)', words_to_numbers[word], line)

		# delete , from numbers
		line = re_com.sub('', line)

		# replace "\\(\\$25\\)" and "\\$25" with "$25"
		line = re_dol.sub('$\\2', line)
		# replace "\\(20\\%\\)" and "20\\%" with "20%"
		line = re_per.sub('\\2%', line)
		# replace "\\(f\\)" by "f"
		line = re_var.sub('\\1', line)

		# find latex expressions; if they are calculatable, replace by number
		n = re_la.findall(line)
		if n != ():
			for tup in n:
				number = latex_to_decimal(tup[1])
				if number != None:
					line = line.replace(tup[0], number)

		new_element['question'] = element['question']
		new_element['question_mod'] = line
		if 'choices' in element:
			new_choices = {}
			for key in element['choices']:
				option = element['choices'][key]

				new_option = {}
				new_option['text'] = option

				option = preprocessing_answer(option)
				option = extract_from_answer(option)

				new_option['value'] = option
				new_choices[key] = new_option
			new_element['choices'] = new_choices
		# if 'answer' in element:
		# 	right_answer = element['answer']
		# 	if 'choices' in element:
		# 		new_element['answer'] = new_element['choices'][right_answer]
		# 	else:
		# 		new_answer = {}
		# 		new_answer['text'] = right_answer
		# 		new_answer['value'] = extract_from_answer(preprocessing_answer(right_answer))
		# 		new_element['answer'] = new_answer
		new_element['id'] = element['id']

		new_arr.append(new_element)

	return new_arr

def extracting_from_questions(arr):
	new_arr = []

	begin_of_re = '(?:(?<=\\s)|(?<=^))'
	end_of_re = '(?:(?=!|\\(|\\)|;|"|\'|,|\\.|\\?|\\s|:\\s))'

	# regular expressions for extracting:
	# Latex expressions
	re_la = '\\\\\\((?:.+?\\=\\s?)?(.+?)(?:)\\\\\\)'
	# numbers with "."
	re_dot = '[0-9]+\\.[0-9]+'
	# normal numbers
	re_nor = '[0-9]+'
	# numbers with "$" sign
	re_dol = '\\$(' + re_dot + '|' + re_nor + ')'
	# numbers with "%" sign
	re_per = '(' + re_dot + '|' + re_nor + ')%'
	# number-unit (e.g. 13-inch)
	re_nu = '(' + re_dot + '|' + re_nor + ')\\-[a-zA-Z]+'
	# time
	re_ti = '([0-9]{1,2}:[0-9]{2})'
	# variables - small letters except "a"
	re_var = '([b-z])'

	# final regex - a combination of all regexes
	final_re = re.compile(begin_of_re + '(?:' + re_per + '|' + re_dol + '|' + re_nu + '|(' + re_dot + ')|' + re_la + '|(' + re_nor + ')|' + re_var + '|' + re_ti + ')' + end_of_re)

	for element in arr:
		# array for extracted quantities
		quantities = []
		# question modified by preprocessing
		line = element['question_mod']

		# find all quantities and extract them; write every quantity in a dictionary, write the dictionary in an array
		n = final_re.findall(line)
		if n != ():
			for tup in n:
				quantity = {}
				for i in range(len(tup)):
					if tup[i] != '':
						quantity['value'] = tup[i]
						break
				# add dictionary with quantity to the array of all quantities
				quantities.append(quantity)

		# print(quantities)
		# new_element = dict(element)
		new_element = {}
		new_element['id'] = element['id']
		new_element['question'] = element['question']
		new_element['question_mod'] = element['question_mod']
		new_element['quantities'] = quantities
		# new_element['answer'] = element['answer']
		if 'choices' in element:
			new_element['choices'] = element['choices']
		new_arr.append(new_element)

	return new_arr

# running on whole training set
# with open('../semeval-2019-task-10-master/data_analysis/open_tag.json') as file:
with open('./open.test.json') as file:
	questions = json.load(file)

new_questions = preprocessing_questions(questions)
new_questions = extracting_from_questions(new_questions)

# with open('./open.train_retrieved.json', 'w') as file:
with open('./open.test_retrieved.json', 'w') as file:
	json.dump(new_questions, file, indent=4)
