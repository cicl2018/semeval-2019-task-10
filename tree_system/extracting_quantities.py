import re
import json
import numpy

def preprocessing_answers(answer):
	begin_of_re = '(?:(?<=\\s)|(?<=^))'
	end_of_re = '(?=(?:(!|\\(|\\)|:|;|"|\'|,|\\.|\\?|\\s|$)))'

	# deleting , in numbers (e.g. 96,000)
	re_com = re.compile('(?<=[0-9]),(?=[0-9])')

	# array for changing all the numbers written with words into numerical forms
	words_to_numbers = {'(o|O)ne': '1', '(t|T)wo': '2', '(t|T)hree': '3', '(f|F)our': '4', '(f|F)ive': '5', '(s|S)ix': '6', '(s|S)even': '7', '(e|E)ight': '8', '(n|N)ine': '9', '(t|T)en': '10', '(e|E)leven': '11', '(t|T)welve': '12', '(t|T)hirteen': '13', '(f|F)ourteen': '14', '(s|S)ixteen': '16', '(s|S)eventeen': '17', '(e|E)ighteen': '18', '(n|N)ineteen': '19', '(t|T)wenty': '20', '(t|T)hirty': '30', '(f|F)ourty': '40', '(f|F)ifty': '50', '(s|S)ixty': '60', '(s|S)eventy': '70', '(e|E)ighty': '80', '(n|N)inety': '90'}

	# change all the numbers written with words into numerical forms
	for word in words_to_numbers:
		answer = re.sub(begin_of_re + word + end_of_re, words_to_numbers[word], answer)

	# delete , from numbers
	answer = re_com.sub('', answer)

	return answer

def preprocessing_questions(arr):
	new_arr = []

	begin_of_re = '(?:(?<=\\s)|(?<=^))'
	end_of_re = '(?:[!\\(\\):;"\',\\.\\?\\s])'

	#regular expressions for:
	# deleting the parentheses in the end of the problem
	re_par = re.compile('\\(.+?(\\)\\.?$)')
	# replacing "once" by "1 time", "twice" - by "2 times"
	re_once = re.compile(end_of_re + '[^(at)]\\sonce' + end_of_re)
	# deleting (1), (2) etc.
	re_num = re.compile('\\s\\([0-9]+\\)' + end_of_re)
	# deleting , in numbers (e.g. 96,000)
	re_com = re.compile('(?<=[0-9]),(?=[0-9])')

	# array for changing all the numbers written with words into numerical forms
	words_to_numbers = {'(o|O)ne': '1', '(t|T)wo': '2', '(t|T)hree': '3', '(f|F)our': '4', '(f|F)ive': '5', '(s|S)ix': '6', '(s|S)even': '7', '(e|E)ight': '8', '(n|N)ine': '9', '(t|T)en': '10', '(e|E)leven': '11', '(t|T)welve': '12', '(t|T)hirteen': '13', '(f|F)ourteen': '14', '(s|S)ixteen': '16', '(s|S)eventeen': '17', '(e|E)ighteen': '18', '(n|N)ineteen': '19', '(t|T)wenty': '20', '(t|T)hirty': '30', '(f|F)ourty': '40', '(f|F)ifty': '50', '(s|S)ixty': '60', '(s|S)eventy': '70', '(e|E)ighty': '80', '(n|N)inety': '90'}


	for element in arr:
		line = element['question']
		new_element = {}

		# delete the parentheses in the end of the problem
		line = re_par.sub('', line)

		# replace "once" by "1 time", "twice" - by "2 times"
		line = re_once.sub(' 1 time', line)
		line = re.sub('\\stwice' + end_of_re, ' 2 times ', line)

		# delete (1), (2) etc.
		line = re_num.sub(' ', line)

		# change all the numbers written with words into numerical forms
		for word in words_to_numbers:
			line = re.sub(begin_of_re + word + '(?=' + end_of_re + '|\\-)', words_to_numbers[word], line)

		# delete , from numbers
		line = re_com.sub('', line)

		new_element['question'] = element['question']
		new_element['question_mod'] = line
		right_answer = element['answer']
		if 'choices' in element:
			# new_element['answer'] = element['choices'][right_answer]
			answer = element['choices'][right_answer]
			new_element['answer'] = preprocessing_answers(answer)
		else:
			new_element['answer'] = right_answer
		new_element['id'] = element['id']

		new_arr.append(new_element)

		# print(line)

	return new_arr

def extracting_answers(line):
	begin_of_re = '(?:(?<=\\s)|(?<=^))'
	end_of_re = '(?:!|\\(|\\)|;|"|\'|,|\\.|\\?|\\s|:\\s|$)'

	#regular expressions for extracting:
	# small letters except a, in constructions like \\(p\\)
	re_sl1 = '\\\\\\(([b-z])\\\\\\)'
	# small letters except a
	re_sl2 = '([b-z])'
	# Latex expressions
	# re_la = '\\\\\\((.+?)(?:)\\\\\\)'
	re_la = '\\\\\\((?:.+?\\=\\s?)?(.+?)(?:)\\\\\\)'
	# ratios
	# re_rat = '([0-9]+:[0-9]+)'
	# numbers with ","
	re_com = '[0-9]+,[0-9]+'
	# numbers with "."
	re_dot = '[0-9]+\\.[0-9]+'
	# normal numbers
	re_nor = '[0-9]+'
	# numbers with "$" sign
	re_dol = '(?:\\\\\\()?(?:\\\\)?(\\$)' + '(' + re_com + '|' + re_dot + '|' + re_nor + ')(?:\\\\\\))?'
	# re_dol = '(?:\\\\)?(\\$)' + '(' + re_com + '|' + re_dot + '|' + re_nor + ')'
	# numbers with "%" sign
	re_per = '(?:\\\\\\()?(' + re_com + '|' + re_dot + '|' + re_nor + ')(?:\\\\)?(%)(?:\\\\\\))?'
	# re_per = '(' + re_com + '|' + re_dot + '|' + re_nor + ')(?:\\\\)?(%)'
	# number-unit (e.g. 13-inch)
	re_nu = '(' + re_com + '|' + re_dot + '|' + re_nor + ')\\-([a-zA-Z]+)'
	# time
	re_ti = '([0-9]{1,2}:[0-9]{2})'

	# final regex - a combination of all regexes
	final_re = re.compile(begin_of_re + '(?:' + re_per + '|' + re_dol + '|' + re_nu + '|(' + re_dot + ')|(' + re_com + ')|' + re_la + '|(' + re_nor + ')|' + re_sl1 + '|' + re_sl2 + '|' + re_ti + ')' + end_of_re) 

	# array for extracted quantities
	quantities = []

	# write every quantity and possibly its unit into an array
	n = final_re.findall(line)
	if n != ():
		for tup in n:
			# print(line)
			quantity = ['', '']
			for i in range(len(tup)):
				if tup[i] != '':
					if tup[i] == '$':
						quantity[1] = '$'
						quantity[0] = tup[i+1]
						break
					elif i < (len(tup) - 1):
						quantity[0] = tup[i]
						if tup[i+1] != '':
							quantity[1] = tup[i+1]
						break
					else:
						quantity[0] = tup[i]
			# print(quantity)
			# add array with quantity and possibly its unit to the array of all quantities
			quantities.append(quantity)

	# this block turns latex fractions into floats
	for quantity in quantities:
		number1_found = False
		number2_found = False
		if quantity[0].startswith("\\frac"):
			fraction = quantity[0]
			print("fraction found")
			for i in range(4, len(fraction)):
				if fraction[i] == '{' and not number1_found:
					print('n1 start')
					start_index = i
				if fraction[i] == '}' and not number1_found:
					end_index = i
					number1_found = True
					print("n1 found")
				if number1_found:
					print(start_index, end_index)
					number1 = fraction[start_index + 2: end_index - 1]
					print(number1)
					break

			for i in range(end_index + 1, len(fraction)):
				if fraction[i] == '{' and number1_found and not number2_found:
					print('n2 start')
					start_index = i
				if fraction[i] == '}' and number1_found:
					end_index = i
					number2_found = True
					print("number2 found")
				if number2_found:
					number2 = fraction[start_index + 2: end_index - 1]
					print(number2)
					break

			if number1_found and number2_found and number1.isdigit() and number2.isdigit():
				quantity[0] = str(numpy.round(int(number1) / int(number2), decimals=2))
				print(quantity[0])

	return quantities

def extracting_questions(arr):
	new_arr = []
	
	begin_of_re = '(?:(?<=\\s)|(?<=^))'
	end_of_re = '(?:[!\\(\\);"\',\\.\\?\\s]|:\\s)'

	#regular expressions for extracting:
	# small letters except a, in constructions like \\(p\\)
	re_sl1 = '\\\\\\(([b-z])\\\\\\)'
	# small letters except a
	re_sl2 = '([b-z])'
	# Latex expressions
	# re_la = '\\\\\\((.+?)(?:)\\\\\\)'
	re_la = '\\\\\\((?:.+?\\=\\s?)?(.+?)(?:)\\\\\\)'
	# ratios
	# re_rat = '([0-9]+:[0-9]+)'
	# numbers with ","
	re_com = '[0-9]+,[0-9]+'
	# numbers with "."
	re_dot = '[0-9]+\\.[0-9]+'
	# normal numbers
	re_nor = '[0-9]+'
	# numbers with "$" sign
	re_dol = '(?:\\\\\\()?(?:\\\\)?(\\$)' + '(' + re_com + '|' + re_dot + '|' + re_nor + ')(?:\\\\\\))?'
	# re_dol = '(?:\\\\)?(\\$)' + '(' + re_com + '|' + re_dot + '|' + re_nor + ')'
	# numbers with "%" sign
	re_per = '(?:\\\\\\()?(' + re_com + '|' + re_dot + '|' + re_nor + ')(?:\\\\)?(%)(?:\\\\\\))?'
	# re_per = '(' + re_com + '|' + re_dot + '|' + re_nor + ')(?:\\\\)?(%)'
	# number-unit (e.g. 13-inch)
	re_nu = '(' + re_com + '|' + re_dot + '|' + re_nor + ')\\-([a-zA-Z]+)'
	# time
	re_ti = '([0-9]{1,2}:[0-9]{2})'

	# final regex - a combination of all regexes
	final_re = re.compile(begin_of_re + '(?:' + re_per + '|' + re_dol + '|' + re_nu + '|(' + re_dot + ')|(' + re_com + ')|' + re_la + '|(' + re_nor + ')|' + re_sl1 + '|' + re_sl2 + '|' + re_ti + ')' + end_of_re) 

	# open file for writing preprocessed questions and quantities (for checking)
	# file = open('quantities.txt', 'w')

	for element in arr:
		# array for extracted quantities
		quantities = []
		# question modified by preprocessing
		line = element['question_mod']

		# write question to file for checking
		# file.write(line + '\n')

		# find all quantities and extract them / them and their units
		# write every quantity and possibly its unit into an array
		n = final_re.findall(line)
		if n != ():
			for tup in n:
				quantity = ['', '']
				for i in range(len(tup)):
					if tup[i] != '':
						if tup[i] == '$':
							quantity[1] = '$'
							quantity[0] = tup[i+1]
							break
						elif i < (len(tup) - 1):
							quantity[0] = tup[i]
							if tup[i+1] != '':
								quantity[1] = tup[i+1]
							break
						else:
							quantity[0] = tup[i]
				# add array with quantity and possibly its unit to the array of all quantities
				quantities.append(quantity)

		# create new dictionary and write it to array
		new_element = {}
		new_element['question'] = element['question']
		new_element['id'] = element['id']
		new_element['answer'] = {}
		new_element['answer']['quantities'] = extracting_answers(element['answer'])
		new_element['answer']['text'] = element['answer']
		
		new_quantities = []
		new_quantity = {}
		# write quantities and possibly their units to new_quantity; add new_quantity to array of quantities
		for quantity in quantities:
			#this block turns latex fractions into floats
			number1_found = False
			number2_found = False
			if quantity[0].startswith("\\frac"):
				fraction = quantity[0]
				print("fraction found")
				for i in range(4, len(fraction)):
					if fraction[i] == '{' and not number1_found:
						print('n1 start')
						start_index = i
					if fraction[i] == '}' and not number1_found:
						end_index = i
						number1_found = True
						print("n1 found")
					if number1_found:
						print(start_index, end_index)
						number1 = fraction[start_index + 2 : end_index - 1]
						print(number1)
						break

				for i in range(end_index + 1, len(fraction)):
					if fraction[i] == '{' and number1_found and not number2_found:
						print('n2 start')
						start_index = i
					if fraction[i] == '}' and number1_found:
						end_index = i
						number2_found = True
						print("number2 found")
					if number2_found:
						number2 = fraction[start_index + 2: end_index - 1]
						print(number2)
						break

				if number1_found and number2_found and number1.isdigit() and number2.isdigit():
					quantity[0] = str(numpy.round(int(number1) / int(number2), decimals=2))
					print(quantity[0])
			#block ends
			# print(quantity[0] + ' ' + quantity[1] + ', ')
			new_quantity['value'] = quantity[0]
			new_quantity['unit'] = quantity[1]
			new_quantities.append(new_quantity)
			new_quantity = {}

		# add new_quantity to new_element; add new_element to array of questions
		new_element['quantities'] = new_quantities
		new_arr.append(new_element)

		new_quantities = []

		# write to file for checking
		# for quantity in quantities:
		# 	file.write(quantity[0] + ' ' + quantity[1] + ', ')
		# file.write('\n\n')

	return new_arr

	# close file for checking
	# file.close()

# running on test example
# testline = 'Last Christmas $1.50, $2,000, $20, 1.5%, 2,000%, 20%, \\$30, 30\\%, 13-inch, 13.5-inch, 3,000-inch, 56, 3.5, 3,000, \\(13 \\frac{1}{16}\\), \\(n = (x)2^{\\frac{t}{3}}\\), \\(p\\), m I gave your my heart'
# extracting([testline])

# running on whole training set
with open('../data_analysis/open_tag.json') as file:
	questions = json.load(file)

new_questions = preprocessing_questions(questions)
new_questions = extracting_questions(new_questions)

with open('./modified_questions.json', 'w') as file:
	json.dump(new_questions, file, indent= 4)