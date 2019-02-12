from my_tree import Node
from building_trees import enum_unordered, operations_for_nodes, calculate_tree, check_monotomic
import json
from itertools import combinations

# given an array of quantities and an answer, return trees that give the right answer to question
def get_gold_trees(arr, answer, ifReverse):
	# generate all possible trees with the amount of quantities from 2 till the total number of quantities
	enum_trees = []
	for length in range(2, len(arr) + 1):
		for temp_arr in combinations(arr, length):
			for tree in enum_unordered(temp_arr):
				enum_trees.append(tree)

	# print(len(enum_trees))

	# fill every tree with all possible combinations of operation signs
	oper_trees = []
	for enum_tree in enum_trees:
		for oper_tree in operations_for_nodes(enum_tree, ifReverse):
			oper_trees.append(oper_tree)

	# print(len(oper_trees))

	# exclude non-monotomic trees
	right_trees = []
	for tree in oper_trees:
		if check_monotomic(tree, ifReverse):
			right_trees.append(tree)

	# print(len(right_trees))

	# calculate trees and choose the ones that gave the right result
	gold_trees = []
	for tree in right_trees:
		tree_answer = calculate_tree(tree, ifReverse)
		# compare to the right answer
		if tree_answer == answer:
			gold_trees.append(tree)

	# if there is the only one tree that gives the right result
	if len(gold_trees) == 1:
		return gold_trees

	# if there are several trees that give the right result
	elif len(gold_trees) > 1:
		# eliminate quantity if its value is 1.0
		new_arr = []

		first_element = arr[0]
		if type(first_element) is dict:
			for element in arr:
				if element["value"] != 1.0:
					new_arr.append(element)
		else:
			for element in arr:
				if element != 1.0:
					new_arr.append(element)
		if len(new_arr) < len(arr):
			gold_trees_new = get_gold_trees(new_arr, answer, ifReverse)
			if len(gold_trees_new) > 0 and len(gold_trees_new) < len(gold_trees):
				return gold_trees_new
			return gold_trees

		# if there is no quantity with 1.0 as value, leave only trees with the maximum number of elements
		else:
			new_gold_trees = []
			max_leaves = gold_trees[-1].leaves_number()

			for tree in gold_trees:
				if tree.leaves_number() == max_leaves:
					new_gold_trees.append(tree)

			return new_gold_trees

	return []

# find questions in training set that can be answered with trees
def process_all_questions(f_input, max_length, f_output, ifReverse):
	with open(f_input) as file:
		questions = json.load(file)

	# variables for statictics
	processed = 0
	solved = 0
	compl = 0
	not_solved = 0
	not_processed = 0
	length_is_more_or_less = 0

	# array for answered questions
	answered_questions = []

	for question in questions:
		quantities = question["quantities"]
		# if number of quantities in the borders and there is only one number in the answer, process answer and quantity values and try to get gold trees for question
		if len(quantities) < max_length and len(quantities) > 1:
			if len(question["answer"]["value"]) == 1:
				try:
					answer = float(question["answer"]["value"][0])

					arr_q = []
					for quantity in quantities:
						q = float(quantity["value"])
						arr_q.append(q)

					processed +=1

					print(question["question_mod"])

					result = get_gold_trees(arr_q, answer, ifReverse)

					# print(str(len(result)) + "\n")
					print("\n")

					# fill array with answered questions if there are gold trees and , depending on result, add numbers to variables
					if len(result) == 1:
						answered_questions.append(question)
						solved += 1
					elif len(result) > 1:
						answered_questions.append(question)
						compl += 1
					else:
						not_solved += 1

				except ValueError:
					not_processed += 1
			else:
				not_processed += 1
		else:
			length_is_more_or_less += 1

	# print out statistics
	print("Processed: " + str(processed))
	print("Solved: " + str(solved))
	print("Complex:" + str(compl))
	print("Not solved: " + str(not_solved))
	print("\nNot processed: " + str(not_processed)) 
	print("length_is_more: " + str(length_is_more_or_less))

	# write an array of answered questions to file if name of file was specified
	if f_output:
		with open(f_output, 'w') as file:
			json.dump(answered_questions, file, indent=4)

# given a triple consisting of two quantities and their operation, make a line with their features for lca table (for training lca classifier)
def lca_table_line(triple, id, q_comp_tokens, q_rate, ifAnswer):
	q1 = triple["q1"]
	q2 = triple["q2"]

	line = str(id) + "\t" + str(q1["value"]) + "\t" + str(q2["value"]) + "\t" + str(q1["verb"]) + "\t" + str(q2["verb"]) + "\t" + str(q1["if_rate_in_q"]) + '\t' + str(q2["if_rate_in_q"]) + '\t' + str(q1["adverbs"]) + '\t' + str(q2["adverbs"]) + "\t"

	if q1["rate"] != None:
		if q1["unit"] != None:
			unit1 = q1["unit"] + " " + q1["rate"]
		else:
			unit1 = q1["rate"]
		if_rate1 = True
	else:
		unit1 = q1["unit"]
		if_rate1 = False

	if q2["rate"] != None:
		if q2["unit"] != None:
			unit2 = q2["unit"] + " " + q2["rate"]
		else:
			unit2 = q2["rate"]
		if_rate2 = True
	else:
		unit2 = q2["unit"]
		if_rate2 = False

	if if_rate1 == True and if_rate2 == False:
		if unit2 == q1["unit"]:
			which_unit_comp = 1
		if unit2 == q1["rate"]:
			which_unit_comp = 2
		else:
			which_unit_comp = None
	elif if_rate1 == False and if_rate2 == True:
		if unit1 == q2["unit"]:
			which_unit_comp = 1
		if unit1 == q2["rate"]:
			which_unit_comp = 2
		else:
			which_unit_comp = None
	else:
		which_unit_comp = None

	same_unit = True if unit1 == unit2 else False
	same_verb = True if q1["verb"] == q2["verb"] and q1["verb"] != None else False
	if_greater = True if q1["value"] > q2["value"] else False


	# if there is a label (for training data)
	if ifAnswer:
		operation = triple["operation"]
		line += str(if_rate1) + '\t' + str(if_rate2) + '\t' + str(same_verb) + '\t' + str(same_unit) + '\t' + str(which_unit_comp) + '\t' + str(if_greater) + '\t' + str(q_comp_tokens) + '\t' + str(q_rate) + '\t' + operation + '\n'
	else:
		line += str(if_rate1) + '\t' + str(if_rate2) + '\t' + str(same_verb) + '\t' + str(same_unit) + '\t' + str(which_unit_comp) + '\t' + str(if_greater) + '\t' + str(q_comp_tokens) + '\t' + str(q_rate) + '\n'

	return line

# given a quantity and its relevance, make a line for irr table (for training relevance classifier)
def rel_table_line(q, id, num_max_matches, num_quantities, ifRelevance, relevance=None):
	line = str(id) + '\t' + str(q["value"]) + '\t'

	if_unit_in_q = True if q["if_unit_in_q"] > 0 else False
	line += str(if_unit_in_q) + '\t' + str(q["other_unit_matches_better"]) + '\t'

	noun_in_q = True if q["noun_in_q"] > 0 else False
	line += str(noun_in_q) + '\t' + str(q["other_noun_matches_better"]) + '\t'

	if ifRelevance:
		line += str(num_max_matches) + '\t' + str(num_quantities) + '\t' + str(relevance) + '\n'
	else:
		line += str(num_max_matches) + '\t' + str(num_quantities) + '\n'

	return line

# for questions in training set that can be answered, make tables for training classifiers
def tables_for_answered_questions(f_input, relevance_table_name, lca_table_name, ifReverse):
	with open(f_input) as file:
		questions = json.load(file)

	rel_table = "id\tq\tif_unit_in_q\tother_unit_matches_better\tnoun_in_q\tother_noun_matches_better\tnum_max_matches\tnum_quantities\trelevance\n"
	lca_table = "id\tq1\tq2\tverb1\tverb2\tif_rate1\tif_rate2\tif_rate_in_q1\tif_rate_in_q2\tadverbs1\tadverbs2\tsame_verb\tsame_unit\twhich_unit_comp\tis_greater\tq_comp_tokens\tq_rate\toperation\n"

	for question in questions:
		quantities = question["quantities"]

		# print(question["question_mod"])
		
		answer = float(question["answer"]["value"][0])
		arr_q = []
		for quantity in quantities:
			q = float(quantity["value"])
			new_q = dict(quantity)
			new_q["value"] = q
			arr_q.append(new_q)

		result = get_gold_trees(arr_q, answer, ifReverse)

		# if for some reason one of answered questions didn't get answered this time
		if result == []:
			print(question["question_mod"])

		# fill relevance table
		for tree in result:
			leaves = tree.get_leaves()

			for quantity in arr_q:
				if quantity not in leaves:
					rel_table += rel_table_line(quantity, question["id"], question["num_max_matches"], len(quantities), True, False)
				else:
					rel_table += rel_table_line(quantity, question["id"], question["num_max_matches"], len(quantities), True, True)

		# fill lca table
		for tree in result:
			arr_triples = tree.get_triples()
			
			for triple in arr_triples:
				lca_table += lca_table_line(triple, question["id"], question["q_comp_tokens"], question["q_rate"], True)

	# write relevance table and lca table
	with open(relevance_table_name, "w") as file:
		file.write(rel_table)

	with open(lca_table_name, "w") as file:
		file.write(lca_table) 

# process_all_questions("./files/open.train_retrieved.json", 7, "./files/open.train_answered.json", False)
# process_all_questions("./files/open.train_retrieved.json", 7, "./files/open.train_answered_with-reverse.json", True)

# tables_for_answered_questions("./files/open.train_answered_features.json", "./files/relevance_train.csv", "./files/lca_train.csv")
tables_for_answered_questions("./files/open.train_answered_with-reverse_features.json", "./files/relevance_train_with-reverse.csv", "./files/lca_train_with-reverse.csv", True)