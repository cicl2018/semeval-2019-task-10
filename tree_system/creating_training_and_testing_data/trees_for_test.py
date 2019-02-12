import json
from my_tree import Node
from all_possible_trees import all_trees_for_question
from trees_for_train import lca_table_line, rel_table_line

# fills relevance table with all possible pairs of quantities for question
def all_possible_pairs(arr_q, id, q_comp_tokens, q_rate):
	lines = ""
	for i in range(len(arr_q)-1):
		for l in range (i+1, len(arr_q)):
			new_pair = {}
			new_pair["q1"] = arr_q[i]
			new_pair["q2"] = arr_q[l]
			lines += lca_table_line(new_pair, id, q_comp_tokens, q_rate, False)
	return lines

# makes tables for question from test set
def tables_for_test_questions(filename):
	with open(filename) as file:
		questions = json.load(file)

	lca_table = "id\tq1\tq2\tverb1\tverb2\tif_rate1\tif_rate2\tif_rate_in_q1\tif_rate_in_q2\tadverbs1\tadverbs2\tsame_verb\tsame_unit\twhich_unit_comp\tis_greater\tq_comp_tokens\tq_rate\n"
	rel_table = "id\tq\tif_unit_in_q\tother_unit_matches_better\tnoun_in_q\tother_noun_matches_better\tnum_max_matches\tnum_quantities\n"

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

					rel_table += rel_table_line(new_q, question["id"], question["num_max_matches"], len(quantities), False)

				all_trees = all_trees_for_question(arr_q, False)
				
				lca_table += all_possible_pairs(arr_q, question["id"], question["q_comp_tokens"], question["q_rate"])

			except ValueError:
				pass

	with open("./files/lca_test_new.csv", "w") as file:
		file.write(lca_table)

	with open("./files/relevance_test_new.csv", "w") as file:
		file.write(rel_table)

tables_for_test_questions("./files/open.test_features.json")