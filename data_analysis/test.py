import json
from pprint import pprint
import re

with open('test.json') as f:
    data = json.load(f)

# y = x['A']
def is_answer_num(data):
	if 'choices' in data:
		if 'A' in data['choices'] and not is_number(data['choices']['A']):
			return False
		if 'B' in data['choices'] and not is_number(data['choices']['B']):
			return False
		if 'C' in data['choices'] and not is_number(data['choices']['C']):
			return False
		if 'D' in data['choices'] and not is_number(data['choices']['D']):
			return False
		if 'E' in data['choices'] and not is_number(data['choices']['E']):
			return False
		return True
	return False

# def is_answer_num(data):
# 	if 'choices' in data:
# 		data['choices']
# 	return True


def is_number(s):
	match = False
	# print(s)
	pattern_straight_num = re.compile("[+-]?[\d]+")
	#straight number
	if pattern_straight_num.match(s):
		match = True

	pattern_quantity_num = re.compile("[\D]*[\d]+[\D]*")
	#quantity number
	if pattern_quantity_num.match(s):
		match = True

	return match


# print(data)
# print(type(data))

# for one_data in data:
	# print(is_answer_num(one_data))
	# print(one_data['choices']['A'])
# pprint(data[3]['choices']['A'])
# pprint(is_number("\\(\\frac { 13 } { 42 } \\)"))
a = re.compile("[\D]*[\d]+[\D]*")
print(a.match("asdf12asd12"))


# pprint(is_number("I only"))


