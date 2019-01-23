from keras.layers import Dense, Dropout
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import csv
from keras.models import Sequential


"""
Preprocesses the data from a table for the MLP
"""
def preprocess(file):
    input = open(file, 'r')

    csvreader = csv.DictReader(input)

    feature1 = []
    feature2 = []
    quantity1 = []
    quantity2 = []
    quantities = []
    ancestors = []
    operations = []
    ids = []

    #fill the column arrays with corresponding values
    for row in csvreader:
        feature1.append([row['Feature1']])
        feature2.append([row['Feature2']])
        quantity1.append([row['Quantity1']])
        quantity2.append([row['Quantity2']])
        quantities.append((row['Quantity1'], row['Quantity2']))
        ancestors.append([row['Operation']])
        ids.append(row['ID'])

        if row['Operation'] not in operations:
            operations.append(row['Operation'])


    #transform the features to onehot
    feature1_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    feature2_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    quantity1_enc = OneHotEncoder(sparse=False, categories='auto', handle_unknown='ignore')
    quantity2_enc = OneHotEncoder(sparse=False, categories='auto', handle_unknown='ignore')

    feature1_enc.fit(feature1)
    feature2_enc.fit(feature2)
    quantity1_enc.fit(quantity1)
    quantity2_enc.fit(quantity2)

    feature1 = feature1_enc.transform(feature1)
    feature2 = feature2_enc.transform(feature2)
    quantity1 = quantity1_enc.transform(quantity1)
    quantity2 = quantity2_enc.transform(quantity2)


    x = []

    for items in zip(feature1, feature2, quantity1, quantity2):
        row = np.concatenate(items, axis=0)
        x.append(row)

    return np.asarray(x), ancestors, operations, quantities, ids


def build_model(x,y):
    mlp = Sequential()
    mlp.add(Dense(units=64, activation="relu"))
    mlp.add(Dense(units=3, activation='softmax'))
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
    x, y, operations, quantities, ids = preprocess('dummy_table_ancestor.csv')
    answers = y
    # transform the answers to onehot
    y_enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    y_enc.fit(y)
    y = y_enc.transform(y)
    categories = y_enc.categories_[0]
    mlp = build_model(x, y)
    preds, categories = predict_operations(mlp, x, quantities, ids, categories)
    print(preds)
    predis = mlp.predict(x)
    acc_string, acc_number = accuracy(predis, answers, categories)
    mlp.save('ancestor_mlp.h5')
    print(acc_string)
    print(acc_number)



