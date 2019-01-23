from my_tree import Node
from building_trees import enum_unordered, operations_for_nodes, calculate_tree, check_monotomic
import json
from itertools import combinations

# returns all possible non-monotomic trees for an array of quantities
def all_trees_for_question(arr):
	enum_trees = []

	# generate all possible trees with the amount of quantities from 2 till the total number of quantities
	for length in range(2, len(arr) + 1):
		for temp_arr in combination(arr, length):
			for tree in enum_unordered(temp_arr):
				enum_trees.append(tree)

	# fill every tree with all possible combinations of operation signs
	oper_trees = []
	for enum_tree in enum_trees:
		for oper_tree in operations_for_nodes(enum_tree):
			oper_trees.append(oper_tree)

	# exclude non-monotomic trees
	right_trees = []
	for tree in oper_trees:
		if check_monotomic(tree):
			right_trees.append(tree)

	return right_trees

def all_trees_for_all_questions(filename):
	with open(filename) as file:
		questions = json.load(file)

	for question in questions:
		quantities = question["quantities"]
		if len(quantities) < 7 and len(quantities) > 1:
			try:
				arr_q = []
				for quantity in quantities:
					q = float(quantity["value"])
					new_q = dict(quantity)
					new_q["value"] = q
					arr_q.append(new_q)

				all_trees = all_trees_for_question(arr_q)

