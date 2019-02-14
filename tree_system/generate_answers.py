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
    mlp_relevances = load_model('relevance_mlp.h5')
    rel_x, rel_y, rel_quantities, rel_ids, test_rel_x, test_rel_quantities, test_rel_ids = rel.preprocess('relevance_train_with-reverse.csv', 'relevance_test.csv')
    relevances = rel.predict_relevances(mlp_relevances, test_rel_x, test_rel_quantities, test_rel_ids)

    #get most likely common ancestor ratings
    mlp_ancestors = load_model('ancestor_mlp.h5')
    anc_x, y, operations, anc_quantities, anc_ids, test_x, test_quantities, test_ids = anc.preprocess('lca_train.csv', 'lca_test.csv')
    y_enc = OneHotEncoder(sparse=False)
    y_enc.fit(y)
    y = y_enc.transform(y)
    categories = list(y_enc.categories_[0])
    ancestors, categories = anc.predict_operations(mlp_ancestors, test_x, test_quantities, test_ids, categories)
    print('Building a bunch of trees')
    possible_trees = all_trees_for_all_questions('open.test_features.json', ifReverse=False)
    print('Evaluating trees')
    ratings = evaluate_trees(possible_trees, relevances, ancestors, categories)
    print("len relevances:", len(relevances))
    print("len ancestors:", len(ancestors))
    input = open('open.test_features.json', 'r')
    questions = json.load(input)
    print('Actually coming up with some answers now')
    print('len ratings:', len(ratings))
    print('len questions:', len(questions))
    for id in ratings.keys():
            ratings[id].sort(key=lambda x: x[1], reverse=True)

    predicted_choices = {}
    final_json = []
    indeces = []
    for question in questions:
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
    print(predicted_choices)
    average = 0
    for index in indeces:
        average += index[1]

    print('Average index of first choice found:', average/len(indeces))

    with open("../combine_results/alina_test.json", "w+") as f:
        final_output = json.dumps(final_json, indent=4)
        f.write(final_output)