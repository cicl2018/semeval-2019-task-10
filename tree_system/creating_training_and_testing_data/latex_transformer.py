import numpy

def latex_to_decimal(string):
	number0_found = False
	number1_found = False
	number2_found = False
	if string[0].isdigit():
		number0_found = True
		if string[1].isdigit():
			number0 = string[:2]
		else:
			number0 = string[0]
	if "\\frac" in string:
		fraction = string
		for i in range(4, len(fraction)):
			if fraction[i] == '{' and not number1_found:
				start_index = i
			if fraction[i] == '}' and not number1_found:
				end_index = i
				number1_found = True
			if number1_found:
				number1 = fraction[start_index + 2: end_index - 1]
				if not number1.isdigit() or number1 == '0':
					number1 = fraction[start_index + 1: end_index]
				break

		for i in range(end_index + 1, len(fraction)):
			if fraction[i] == '{' and number1_found and not number2_found:
				start_index = i
			if fraction[i] == '}' and number1_found:
				end_index = i
				number2_found = True
			if number2_found:
				number2 = fraction[start_index + 2: end_index - 1]
				if not number2.isdigit() or number2 == '0':
					number2 = fraction[start_index + 1: end_index]
				break

		if number1_found and number2_found and number1.isdigit() and number2.isdigit():
			if number0_found:
				# decimal = str(int(number0) + numpy.round(int(number1) / int(number2), decimals=2))
				decimal = str(int(number0) + int(number1) / int(number2))
				number0_found = False
			else:
				# decimal = str(numpy.round(int(number1) / int(number2), decimals=2))
				decimal = str(int(number1) / int(number2))
		else: return None
	else: return None

	return decimal