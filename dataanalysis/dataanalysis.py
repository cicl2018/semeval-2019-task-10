import json
from pprint import pprint

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

def is_answer_num(data):
	# print type(data['choices'])

	if 'choices' in data and data['choices']['A'] == u'3':
		return True
	return False

# with open('test.json') as f:
with open('sat.train.json') as f:
    data = json.load(f)

# counters
open_tags = 0
closed_tags = 0
answer_num = 0


# open output files
f_closed = open('closed_tag.json', 'w+')
f_open = open('open_tag.json', 'w+')
f_answer_num = open('answer_num.json', 'w+')

# init all list
j_open = [];
j_closed = [];
j_answer_num = [];


# loop for all data
for one_data in data:

	# check if is open tag
	if is_open_tag(one_data):
		open_tags+=1
		j_open.append(one_data)

	# check if is close tag
	if is_closed_tag(one_data):
		closed_tags+=1
		j_closed.append(one_data)

	# check if choices are number
	if is_answer_num(one_data):
		answer_num+=1
		j_answer_num.append(one_data)


# write data in the files
open_output = json.dumps(j_open, indent = 4)
closed_output = json.dumps(j_closed, indent = 4)
answer_num_output = json.dumps(j_answer_num, indent = 4)
print >> f_closed, closed_output
print >> f_open, open_output
print >> f_answer_num, answer_num_output
f_closed.close()
f_open.close()
f_answer_num.close()




#
#
# write a file
#
#
# j = json.dumps(data, indent=4)
# f = open('sample.json', 'w')
# print >> f, j
# f.close()


print "Data Analysis"
print "=============================="
print "Open Questions: " + str(open_tags)
print "Close Questions:" + str(closed_tags)
print "=============================="
