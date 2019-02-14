from keras.layers import Dense, Dropout
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import csv
from keras.models import Sequential


"""
Preprocesses the data from a table for the MLP
"""
def preprocess(file, test):
    train_input = open(file, 'r')

    csvreader = csv.DictReader(train_input, delimiter='\t')

    quantity_feature = []
    quantities = []
    if_unit_in_q = []
    other_unit_matches_better = []
    noun_in_q = []
    other_noun_matches_better = []
    num_max_matches = []
    num_quantities = []
    relevances = []
    relevances_buffer = []
    ids = []
    #fill the column arrays with corresponding values
    for row in csvreader:
        quantity_feature.append([row['q']])
        if_unit_in_q.append([row['if_unit_in_q']])
        other_unit_matches_better.append([row['other_unit_matches_better']])
        noun_in_q.append([row['noun_in_q']])
        other_noun_matches_better.append([row['other_noun_matches_better']])
        num_max_matches.append([row['num_max_matches']])
        num_quantities.append([row['num_quantities']])
        relevances_buffer.append([row['relevance']])
        quantities.append(row['q'])
        ids.append(int(row['id']))

    relevance_true = 0
    relevance_false = 0
    for relevance in relevances_buffer:
        if relevance[0] == 'True':
            relevances.append('1')
            relevance_true += 1
        else:
            relevances.append('0')
            relevance_false += 1

    #transform the features to onehot
    quantity_feature_enc = OneHotEncoder(sparse=False, categories='auto', handle_unknown='ignore')
    if_unit_in_q_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    other_unit_matches_better_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    noun_in_q_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    other_noun_matches_better_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    num_max_matches_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    num_quantities_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')

    quantity_feature_enc.fit(quantity_feature)
    if_unit_in_q_enc.fit(if_unit_in_q)
    other_unit_matches_better_enc.fit(other_unit_matches_better)
    noun_in_q_enc.fit(noun_in_q)
    other_noun_matches_better_enc.fit(other_noun_matches_better)
    num_max_matches_enc.fit(num_max_matches)
    num_quantities_enc.fit(num_quantities)

    quantity_feature = quantity_feature_enc.transform(quantity_feature)
    if_unit_in_q = if_unit_in_q_enc.transform(other_unit_matches_better)
    other_unit_matches_better = other_unit_matches_better_enc.transform(other_unit_matches_better)
    noun_in_q = noun_in_q_enc.transform(noun_in_q)
    other_noun_matches_better = other_noun_matches_better_enc.transform(other_noun_matches_better)
    num_max_matches = num_max_matches_enc.transform(num_max_matches)
    num_quantities = num_quantities_enc.transform(num_quantities)

    x = []

    for items in zip(quantity_feature, if_unit_in_q, other_unit_matches_better, noun_in_q, other_noun_matches_better,
                     num_max_matches, num_quantities):
        row = np.concatenate(items, axis=0)
        x.append(row)

    test_input = open(test, 'r')

    csvreader2 = csv.DictReader(test_input, delimiter='\t')

    test_quantity_feature = []
    test_quantities = []
    test_if_unit_in_q = []
    test_other_unit_matches_better = []
    test_noun_in_q = []
    test_other_noun_matches_better = []
    test_num_max_matches = []
    test_num_quantities = []
    test_ids = []
    #fill the column arrays with corresponding values
    for row in csvreader2:
        test_quantity_feature.append([row['q']])
        test_if_unit_in_q.append([row['if_unit_in_q']])
        test_other_unit_matches_better.append([row['other_unit_matches_better']])
        test_noun_in_q.append([row['noun_in_q']])
        test_other_noun_matches_better.append([row['other_noun_matches_better']])
        test_num_max_matches.append([row['num_max_matches']])
        test_num_quantities.append([row['num_quantities']])
        test_quantities.append(row['q'])
        test_ids.append(int(row['id']))

    #transform the features to onehot
    test_quantity_feature = quantity_feature_enc.transform(test_quantity_feature)
    test_if_unit_in_q = if_unit_in_q_enc.transform(test_other_unit_matches_better)
    test_other_unit_matches_better = other_unit_matches_better_enc.transform(test_other_unit_matches_better)
    test_noun_in_q = noun_in_q_enc.transform(test_noun_in_q)
    test_other_noun_matches_better = other_noun_matches_better_enc.transform(test_other_noun_matches_better)
    test_num_max_matches = num_max_matches_enc.transform(test_num_max_matches)
    test_num_quantities = num_quantities_enc.transform(test_num_quantities)

    test_x = []

    for items in zip(test_quantity_feature, test_if_unit_in_q, test_other_unit_matches_better, test_noun_in_q, test_other_noun_matches_better, test_num_max_matches, test_num_quantities):
        row = np.concatenate(items, axis=0)
        test_x.append(row)
    return np.asarray(x), np.asarray(relevances), quantities, ids, np.asarray(test_x), test_quantities, test_ids


def build_model(x, y):
    mlp = Sequential()
    mlp.add(Dense(units=64, activation="relu"))
    mlp.add(Dropout(0.5))
    mlp.add(Dense(units=1, activation='sigmoid'))
    mlp.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"], validation_split=0.2)
    mlp.fit(x, y, epochs=20, batch_size=32)

    return mlp


def predict_relevances(model, x, quantities, ids):
    predictions = model.predict(x)

    relevances = {}

    for id, quantity, prediction in zip(ids, quantities, predictions):
        if id not in relevances.keys():
            relevances[id] = {float(quantity): prediction[0]}
        else:
            relevances[id][float(quantity)] = prediction[0]

    return relevances


def accuracy(predictions, answers):
    matches = 0
    for prediction, answer in zip(predictions, answers):
        prediction = int(np.round(prediction))
        if prediction == int(answer):
            matches += 1
    accuracy_string = matches, '/', len(answers)
    accuracy_number = np.round(matches / len(y), decimals=4)

    return accuracy_string, accuracy_number


if __name__ == "__main__":

    x, y, quantities, ids, _, _, _ = preprocess('relevance_train_with-reverse.csv', 'relevance_test.csv')
    mlp = build_model(x, y)
    preds = mlp.predict(x)
    acc_string, acc_number = accuracy(preds, y)
    print(acc_string)
    print(acc_number)
    rel_dict = predict_relevances(mlp, x, quantities, ids)
    mlp.save('relevance_mlp.h5')
    print(rel_dict)

