from keras.models import load_model
import relevance_classifier as rel
import ancestor_classifier as anc
from sklearn.preprocessing import OneHotEncoder
from tree_evaluation import evaluate_trees
from building_trees import calculate_tree
from all_possible_trees import all_trees_for_all_questions
from my_tree import Node
import json
import numpy as np

if __name__ == "__main__":
    #get relevance ratings
    #mlp_relevances = load_model('relevance_mlp.h5')
    #rel_x, rel_y, rel_quantities, rel_ids = rel.preprocess('relevance.csv')
    relevances = []#rel.predict_relevances(mlp_relevances, rel_x, rel_quantities, rel_ids)

    #get most likely common ancestor ratings
    mlp_ancestors = load_model('ancestor_mlp.h5')
    anc_x, y, operations, anc_quantities, anc_ids, test_x, test_quantities, test_ids = anc.preprocess('lca.csv', 'lca_to_classify.csv')
    y_enc = OneHotEncoder(sparse=False)
    y_enc.fit(y)
    y = y_enc.transform(y)
    categories = list(y_enc.categories_[0])
    ancestors, categories = anc.predict_operations(mlp_ancestors, test_x, test_quantities, test_ids, categories)
    print('Building a bunch of trees')
    possible_trees = all_trees_for_all_questions('open_modified_features.json')
    print('Evaluating trees')
    ratings = evaluate_trees(possible_trees, relevances, ancestors, categories)

    input = open('open_modified_features.json', 'r')
    questions = json.load(input)
    print('Actually coming up with some answers now')
    predicted_answers = {}

    for id in ratings.keys():
        top10_trees = [(0, 0)] * 9
        for tree_rating in ratings[id]:
            if tree_rating[1] > top10_trees[len(top10_trees) - 1][1]:
                top10_trees[len(top10_trees) - 1] = tree_rating
                top10_trees.sort(key=lambda x: x[1], reverse=True)
        top10_answers = []
        for tree in top10_trees:
            if str(tree[0]).isdigit():
                continue
                top10_answers.append(np.round(calculate_tree(tree[0]), decimals=2))

        predicted_answers[id] = top10_answers

    """
    correct_answers = {}
    correct_choices = {}
    for question in questions:
        if 'choices' not in question.keys():
            continue
        if question['id'] not in correct_answers:
            correct_answers[question['id']] = float(question['answer']['value'][0])
            for choice in question['choices'].keys():
                if not question['choices'][choice]['value']:
                    continue
                if float(question['choices'][choice]['value'][0]) == correct_answers[question['id']]:
                    correct_choices[question['id']] = choice

    matches = 0

    for id in correct_answers.keys():
        id = str(id)
        int_id = int(id)
        if id in predicted_answers.keys():
            results = predicted_answers[id]
            for result in results:
                if result == correct_answers[int_id]:
                    matches += 1
    print(matches, "/", len(predicted_answers))
    print(np.round(matches / len(predicted_answers), decimals=4))
    """
    predicted_choices = {}
    final_json = []

    for question in questions:
        #if str(question['id']) in predicted_answers.keys():
            if 'choices' not in question.keys():
                if str(question['id']) in predicted_answers.keys() and predicted_answers[str(question['id'])]:
                    final_json.append({'id': question['id'], 'answer': str(predicted_answers[str(question['id'])][0])})
                else:
                    continue
            else:
                if str(question['id']) in predicted_answers.keys():
                    choices = []
                    for choice in question['choices']:
                        if not question['choices'][choice]['value']:
                            continue
                        choices.append((choice, question['choices'][choice]['value'][0]))
                    for answer in predicted_answers[str(question['id'])]:
                        choice_found = False
                        for choice in choices:
                            if float(choice[1]) == answer:
                                final_json.append({'id': question['id'], 'answer': choice[0]})
                                predicted_choices[question['id']] = choice[0]
                                choice_found = True
                                break
    print('DONE')
    """
    matches = 0

    for id in correct_choices.keys():
        id = str(id)
        int_id = int(id)
        if id in predicted_choices.keys():
            result = predicted_choices[id]
            if result == correct_choices[int_id]:
                    matches += 1
    print(matches, "/", len(predicted_choices))
    print(np.round(matches / len(predicted_choices), decimals=4))
    """
    with open("alina_test.json", "w+") as f:
        final_output = json.dumps(final_json, indent=4)
        f.write(final_output)