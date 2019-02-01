from keras.models import load_model
import relevance_classifier as rel
import ancestor_classifier as anc
from sklearn.preprocessing import OneHotEncoder
from tree_evaluation import evaluate_trees
from all_possible_trees import all_trees_for_all_questions
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
    ancestors, categories = anc.predict_operations(mlp_ancestors, anc_x, anc_quantities, anc_ids, categories)
    print('Building a bunch of trees')
    possible_trees = all_trees_for_all_questions('answered_questions_new.json')
    print('Evaluating trees')
    ratings = evaluate_trees(possible_trees, relevances, ancestors, categories)

    input = open('answered_questions_new.json', 'r')
    questions = json.load(input)
    print('Actually coming up with some answers now')

    for id in ratings.keys():
            ratings[id].sort(key=lambda x: x[1], reverse=True)

    q_ids = []

    for question in questions:
        q_ids.append(question['id'])

    rate_ids = []

    for rating in ratings:
        rate_ids.append(rating)

    rate_ids.sort()
    q_ids.sort()
    print(rate_ids)
    print(q_ids)

    print(len(rate_ids))
    print(len(q_ids))

    correct_answers = {}
    correct_choices = {}
    for question in questions:
        if question['id'] not in correct_answers.keys():
            correct_answers[question['id']] = float(question['answer']['value'][0])
        if 'choices' not in question.keys():
            continue
        for choice in question['choices'].keys():
            if not question['choices'][choice]['value']:
                continue
            if float(question['choices'][choice]['value'][0]) == correct_answers[question['id']]:
                correct_choices[question['id']] = choice
    print(ratings[10014])
    print(correct_answers)
    matches = 0

    for id in ratings.keys():
        results = ratings[id]
        for result in results:
            if result[0] == correct_answers[id]:
                    matches += 1
                    break
    print(matches, "/", len(ratings))
    print(np.round(matches / len(ratings), decimals=4))

    predicted_choices = {}
    final_json = []
    indeces = []
    for question in questions:
        #if str(question['id']) in ratings.keys():
            if 'choices' not in question.keys():
                if question['id'] in ratings.keys() and ratings[question['id']]:
                    final_json.append({'id': question['id'], 'answer': str(ratings[question['id']][0][0])})
                else:
                    continue
            else:
                if question['id'] in ratings.keys():
                    choices = []
                    for choice in question['choices']:
                        if not question['choices'][choice]['value']:
                            continue
                        choices.append((choice, question['choices'][choice]['value'][0]))
                    for answer in ratings[question['id']]:
                        choice_found = False
                        for choice in choices:
                            if float(choice[1]) == answer[0]:
                                final_json.append({'id': question['id'], 'answer': choice[0]})
                                predicted_choices[question['id']] = choice[0]
                                indeces.append((question['id'], ratings[question['id']].index(answer), choice))
                                choice_found = True
                                break
                        if choice_found:
                            break
    print('DONE')
    print(len(indeces))
    print(indeces)
    print(predicted_choices)
    print(correct_choices)
    matches = 0

    for id in correct_choices.keys():
        if id in predicted_choices.keys():
            result = predicted_choices[id]
            if result == correct_choices[id]:
                    matches += 1
    print(matches, "/", len(ratings))
    print(np.round(matches / len(ratings), decimals=4))

    with open("alina_test.json", "w+") as f:
        final_output = json.dumps(final_json, indent=4)
        f.write(final_output)