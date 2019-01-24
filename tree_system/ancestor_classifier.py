from keras.layers import Dense, Dropout
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import csv
from keras.models import Sequential


"""
Preprocesses the data from a table for the MLP
"""
def preprocess(file, test):
    input = open(file, 'r')

    csvreader = csv.DictReader(input, delimiter='\t')

    quantity1 = []
    quantity2 = []
    quantities = []
    verb1 = []
    verb2 = []
    if_rate1 = []
    if_rate2 = []
    if_rate_in_q1 = []
    if_rate_in_q2 = []
    adverbs1 = []
    adverbs2 = []
    same_verb = []
    same_unit = []
    which_unit_comp = []
    is_greater = []
    q_comp_tokens = []
    q_rate = []
    ancestors = []
    operations = []
    ids = []
    #fill the column arrays with corresponding values
    for row in csvreader:
        quantity1.append([row['q1']])
        quantity2.append([row['q2']])
        verb1.append([row['verb1']])
        verb2.append([row['verb2']])
        if_rate1.append([row['if_rate1']])
        if_rate2.append([row['if_rate2']])
        if_rate_in_q1.append([row['if_rate_in_q1']])
        if_rate_in_q2.append([row['if_rate_in_q2']])
        adverbs1.append([row['adverbs1']])
        adverbs2.append([row['adverbs2']])
        same_verb.append([row['same_verb']])
        same_unit.append([row['same_unit']])
        which_unit_comp.append([row['which_unit_comp']])
        is_greater.append([row['is_greater']])
        q_comp_tokens.append([row['q_comp_tokens']])
        q_rate.append([row['q_rate']])
        ancestors.append([row['operation']])
        quantities.append((row['q1'], row['q2']))
        ids.append(row['id'])

        if row['operation'] not in operations:
            operations.append(row['operation'])


    #transform the training features to onehot
    quantity1_enc = OneHotEncoder(sparse=False, categories='auto', handle_unknown='ignore')
    quantity2_enc = OneHotEncoder(sparse=False, categories='auto', handle_unknown='ignore')
    verb1_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    verb2_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    if_rate_in_q1_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    if_rate_in_q2_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    adverbs1_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    adverbs2_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    if_rate1_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    if_rate2_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    same_verb_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    same_unit_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    which_unit_comp_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    is_greater_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    q_comp_tokens_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    q_rate_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')

    quantity1_enc.fit(quantity1)
    quantity2_enc.fit(quantity2)
    verb1_enc.fit(verb1)
    verb2_enc.fit(verb2)
    if_rate1_enc.fit(if_rate1)
    if_rate2_enc.fit(if_rate2)
    if_rate_in_q1_enc.fit(if_rate_in_q1)
    if_rate_in_q2_enc.fit(if_rate_in_q2)
    adverbs1_enc.fit(adverbs1)
    adverbs2_enc.fit(adverbs2)
    same_verb_enc.fit(same_verb)
    same_unit_enc.fit(same_unit)
    which_unit_comp_enc.fit(which_unit_comp)
    is_greater_enc.fit(is_greater)
    q_comp_tokens_enc.fit(q_comp_tokens)
    q_rate_enc.fit(q_rate)


    quantity1 = quantity1_enc.transform(quantity1)
    quantity2 = quantity2_enc.transform(quantity2)
    verb1 = verb1_enc.transform(verb1)
    verb2 = verb2_enc.transform(verb2)
    if_rate1 = if_rate1_enc.transform(if_rate1)
    if_rate2 = if_rate2_enc.transform(if_rate2)
    if_rate_in_q1 = if_rate_in_q1_enc.transform(if_rate_in_q1)
    if_rate_in_q2 = if_rate_in_q2_enc.transform(if_rate_in_q2)
    adverbs1 = adverbs1_enc.transform(adverbs1)
    adverbs2 = adverbs2_enc.transform(adverbs2)
    same_verb = same_verb_enc.transform(same_verb)
    same_unit = same_unit_enc.transform(same_unit)
    which_unit_comp = which_unit_comp_enc.transform(which_unit_comp)
    is_greater = is_greater_enc.transform(is_greater)
    q_comp_tokens = q_comp_tokens_enc.transform(q_comp_tokens)
    q_rate = q_rate_enc.transform(q_rate)


    x = []

    for items in zip(quantity1, quantity2, verb1, verb2, if_rate1, if_rate2, if_rate_in_q1, if_rate_in_q2, adverbs1,
                     adverbs2, same_verb, same_unit, which_unit_comp, is_greater, q_comp_tokens, q_rate,):
        row = np.concatenate(items, axis=0)
        x.append(row)

    test_input = open(test, 'r')

    csvreader2 = csv.DictReader(test_input, delimiter='\t')

    test_quantity1 = []
    test_quantity2 = []
    test_quantities = []
    test_verb1 = []
    test_verb2 = []
    test_if_rate1 = []
    test_if_rate2 = []
    test_if_rate_in_q1 = []
    test_if_rate_in_q2 = []
    test_adverbs1 = []
    test_adverbs2 = []
    test_same_verb = []
    test_same_unit = []
    test_which_unit_comp = []
    test_is_greater = []
    test_q_comp_tokens = []
    test_q_rate = []
    test_ids = []
    #fill the column arrays with corresponding values
    for row in csvreader2:
        test_quantity1.append([row['q1']])
        test_quantity2.append([row['q2']])
        test_verb1.append([row['verb1']])
        test_verb2.append([row['verb2']])
        test_if_rate1.append([row['if_rate1']])
        test_if_rate2.append([row['if_rate2']])
        test_if_rate_in_q1.append([row['if_rate_in_q1']])
        test_if_rate_in_q2.append([row['if_rate_in_q2']])
        test_adverbs1.append([row['adverbs1']])
        test_adverbs2.append([row['adverbs2']])
        test_same_verb.append([row['same_verb']])
        test_same_unit.append([row['same_unit']])
        test_which_unit_comp.append([row['which_unit_comp']])
        test_is_greater.append([row['is_greater']])
        test_q_comp_tokens.append([row['q_comp_tokens']])
        test_q_rate.append([row['q_rate']])
        test_quantities.append((row['q1'], row['q2']))
        test_ids.append(row['id'])

    test_quantity1 = quantity1_enc.transform(test_quantity1)
    test_quantity2 = quantity2_enc.transform(test_quantity2)
    test_verb1 = verb1_enc.transform(test_verb1)
    test_verb2 = verb2_enc.transform(test_verb2)
    test_if_rate1 = if_rate1_enc.transform(test_if_rate1)
    test_if_rate2 = if_rate2_enc.transform(test_if_rate2)
    test_if_rate_in_q1 = if_rate_in_q1_enc.transform(test_if_rate_in_q1)
    test_if_rate_in_q2 = if_rate_in_q2_enc.transform(test_if_rate_in_q2)
    test_adverbs1 = adverbs1_enc.transform(test_adverbs1)
    test_adverbs2 = adverbs2_enc.transform(test_adverbs2)
    test_same_verb = same_verb_enc.transform(test_same_verb)
    test_same_unit = same_unit_enc.transform(test_same_unit)
    test_which_unit_comp = which_unit_comp_enc.transform(test_which_unit_comp)
    test_is_greater = is_greater_enc.transform(test_is_greater)
    test_q_comp_tokens = q_comp_tokens_enc.transform(test_q_comp_tokens)
    test_q_rate2 = q_rate_enc.transform(test_q_rate)

    test_x = []

    for items in zip(test_quantity1, test_quantity2, test_verb1, test_verb2, test_if_rate1, test_if_rate2, 
    test_if_rate_in_q1, test_if_rate_in_q2, test_adverbs1, test_adverbs2,test_same_verb, test_same_unit, 
    test_which_unit_comp, test_is_greater, test_q_comp_tokens, test_q_rate2,):
        row = np.concatenate(items, axis=0)
        test_x.append(row)

    return np.asarray(x), ancestors, operations, quantities, ids, np.asarray(test_x), test_quantities, test_ids


def build_model(x,y):
    mlp = Sequential()
    mlp.add(Dense(units=64, activation="relu"))
    mlp.add(Dropout(0.5))
    mlp.add(Dense(units=4, activation='softmax'))
    mlp.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"], validation_split=0.2)
    mlp.fit(x, y, epochs=100, batch_size=32)

    return mlp


def predict_operations(model, x, quantities, ids, categories):
    predictions = model.predict(x)

    operations = {}

    for id, quantity, prediction in zip(ids, quantities, predictions):
        if id not in operations.keys():
            operations[id] = {quantity: list(prediction)}
        else:
            operations[id][quantity] = list(prediction)

    return operations, categories

def accuracy(predictions, answers, categories):
    matches = 0
    for prediction, answer in zip(predictions, answers):
        if categories[np.argmax(prediction)] == answer[0]:
            matches += 1
    accuracy_string = matches, '/', len(answers)
    accuracy_number = np.round(matches / len(y), decimals=4)

    return accuracy_string, accuracy_number


if __name__ == "__main__":
    """
    x, y, operations, quantities, ids = preprocess('lca.csv')
    answers = y
    # transform the answers to onehot
    y_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    y_enc.fit(y)
    y = y_enc.transform(y)
    categories = y_enc.categories_[0]
    mlp = build_model(x, y)
    preds, categories = predict_operations(mlp, x, quantities, ids, categories)
    print(categories)
    print(preds)
    predis = mlp.predict(x)
    acc_string, acc_number = accuracy(predis, answers, categories)
    mlp.save('ancestor_mlp.h5')
    print(acc_string)
    print(acc_number)
    """


