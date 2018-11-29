import json
from pprint import pprint
import re

# check if tag is open
def is_open_tag(data):
	if data['tags'] == [u'open']:
		return True
	return False

# check if tag is close
def is_closed_tag(data):
	if data['tags'] == [u'closed']:
		return True
	return False

def is_other_tag(data):
	if data['tags'] == [u'other']:
		return True
	return False

def is_geometry_tag(data):
	if data['tags'] == [u'geometry']:
		return True
	return False

#check if the answers are numerical
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

# check is data has diagram
def has_diagram(data):
	if 'diagramRef' in data:
		return True
	return False

def is_number(s):
	match = False
	# print(s)
	pattern_straight_num = re.compile("[+-]?[\d]+")
	#straight number
	if pattern_straight_num.match(s):
		match = True

	# pattern_quantity_num = re.compile("[\D]*[\d]+[\D]*")
	# #quantity number
	# if pattern_quantity_num.match(s):
	# 	match = True

	return match

# with open('test.json') as f:
with open('sat.train.json') as f:
    data = json.load(f)

# counters
total = 0
open_tags = 0
closed_tags = 0
geometry_tags = 0
other_tags = 0
answer_num = 0
not_answer_num = 0
diagram = 0
not_diagram = 0


# open output files
f_closed = open('closed_tag.json', 'w+')
f_open = open('open_tag.json', 'w+')
f_other = open('other_tag.json', 'w+')
f_geometry = open('geometry_tag.json', 'w+')
f_answer_num = open('answer_num.json', 'w+')
f_not_answer_num = open('not_answer_num.json', 'w+')
f_has_diagram = open('has_diagram.json', 'w+')
f_not_has_diagram = open('not_has_diagram.json', 'w+')

# init all list
l_open = [];
l_closed = [];
l_other = [];
l_geometry = [];
l_answer_num = [];
l_not_answer_num = [];
l_has_diagram = [];
l_not_has_diagram = [];

# loop for all data
for one_data in data:
	total+=1

	# check if is open tag
	if is_open_tag(one_data):
		open_tags+=1
		l_open.append(one_data)

	# check if is close tag
	if is_closed_tag(one_data):
		closed_tags+=1
		l_closed.append(one_data)

	if is_geometry_tag(one_data):
		geometry_tags+=1
		l_geometry.append(one_data)

	if is_other_tag(one_data):
		other_tags+=1
		l_other.append(one_data)

	# check if choices are number
	if is_answer_num(one_data):
		answer_num+=1
		l_answer_num.append(one_data)
	else:
		not_answer_num+=1
		l_not_answer_num.append(one_data)

	if has_diagram(one_data):
		diagram+=1
		l_has_diagram.append(one_data)
	else:
		not_diagram+=1
		l_not_has_diagram.append(one_data)



# write data in the files
open_output = json.dumps(l_open, indent = 4)
closed_output = json.dumps(l_closed, indent = 4)
geometry_output = json.dumps(l_geometry, indent = 4)
other_output = json.dumps(l_other, indent = 4)
answer_num_output = json.dumps(l_answer_num, indent = 4)
not_answer_num_output = json.dumps(l_not_answer_num, indent = 4)
has_diagram_output = json.dumps(l_has_diagram, indent = 4)
not_has_diagram_output = json.dumps(l_not_has_diagram, indent = 4)
# print(closed_output, f_closed)
# print(open_output, f_open)
# print(geometry_output, f_geometry)
# print(other_output, f_other)
# print(answer_num_output, f_answer_num)
# print(has_diagram_output, f_has_diagram)
# print(not_has_diagram_output, f_not_has_diagram)
f_closed.write(closed_output)
f_open.write(open_output)
f_geometry.write(geometry_output)
f_other.write(other_output)
f_answer_num.write(answer_num_output)
f_not_answer_num.write(not_answer_num_output)
f_has_diagram.write(has_diagram_output)
f_not_has_diagram.write(not_has_diagram_output)

f_closed.close()
f_open.close()
f_geometry.close()
f_other.close()
f_answer_num.close()
f_not_answer_num.close()
f_has_diagram.close()
f_not_has_diagram.close()




#
#
# write a file
#
#
# j = json.dumps(data, indent=4)
# f = open('sample.json', 'w')
# print >> f, j
# f.close()
print ("")
print ("")
print ("==============================")
print ("=       Data Analysis        =")
print ("=                            =")
print ("==============================")
print ("Total Questions: " + str(total))
print ("==============================")
print ("Open Questions: " + str(open_tags))
print ("Close Questions: " + str(closed_tags))
print ("Geometry Questions: " + str(geometry_tags))
print ("Other Questions: " + str(other_tags))
print ("==============================")
print ("Numerical Answer Questions: " + str(answer_num))
print ("Not Numerical Answer Questions: " + str(not_answer_num))
print ("==============================")
print ("Diagram Questions: " + str(diagram))
print ("Not a Diagram Questions: " + str(not_diagram))
print ("==============================")
print ("")
print ("")
# 