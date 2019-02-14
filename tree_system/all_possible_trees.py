from my_tree import Node
from building_trees import enum_unordered, operations_for_nodes, calculate_tree, check_monotomic
import json
from itertools import combinations

# returns all possible non-monotomic trees for an array of quantities
def all_trees_for_question(arr, ifReverse):
	enum_trees = []

	# generate all possible trees with the amount of quantities from 2 till the total number of quantities
	for length in range(2, len(arr) + 1):
		for temp_arr in combinations(arr, length):
			for tree in enum_unordered(temp_arr):
				enum_trees.append(tree)

	# fill every tree with all possible combinations of operation signs
	oper_trees = []
	for enum_tree in enum_trees:
		for oper_tree in operations_for_nodes(enum_tree, ifReverse):
			oper_trees.append(oper_tree)

	# exclude non-monotomic trees
	right_trees = []
	for tree in oper_trees:
		if check_monotomic(tree, ifReverse):
			right_trees.append(tree)

	return right_trees

# returns a dictionary where key is question id, and value is all possible trees for quantities of this question
def all_trees_for_all_questions(filename, ifReverse):
	with open(filename) as file:
		questions = json.load(file)
	trees = {}
	for question in questions:
		id = int(question['id'])
		quantities = question["quantities"]
		if not len(quantities) < 6 or not len(quantities) > 1:
			continue
		if len(quantities) < 6 and len(quantities) > 1:
			try:
				arr_q = []
				for quantity in quantities:
					q = float(quantity["value"])
					new_q = dict(quantity)
					new_q["value"] = q
					arr_q.append(new_q)

				all_trees = all_trees_for_question(arr_q, ifReverse)
			except ValueError:
				continue
		trees[id] = all_trees

	return trees
