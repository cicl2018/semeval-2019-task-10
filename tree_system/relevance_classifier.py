from keras.layers import Dense, Dropout
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import csv
from keras.models import Sequential


"""
Preprocesses the data from a table for the MLP
"""
def preprocess(file):
    train_input = open(file, 'r')

    csvreader = csv.DictReader(train_input)

    feature1 = []
    feature2 = []
    quantities_feature = []
    quantities = []
    relevances = []
    ids = []

    #fill the column arrays with corresponding values
    for row in csvreader:
        feature1.append([row['Feature1']])
        feature2.append([row['Feature2']])
        quantities_feature.append([row['Quantity']])
        quantities.append(row['Quantity'])
        relevances.append(row['Relevance'])
        ids.append(row['ID'])

    #transform the features to onehot
    feature1_enc = OneHotEncoder(sparse=False)
    feature2_enc = OneHotEncoder(sparse=False)
    quantities_feature_enc = OneHotEncoder(sparse=False, categories='auto')

    feature1_enc.fit(feature1)
    feature2_enc.fit(feature2)
    quantities_feature_enc.fit(quantities_feature)

    feature1 = feature1_enc.transform(feature1)
    feature2 = feature2_enc.transform(feature2)
    quantities_feature = quantities_feature_enc.transform(quantities_feature)

    x = []

    for items in zip(feature1, feature2, quantities_feature):
        row = np.concatenate(items, axis=0)
        x.append(row)

    return np.asarray(x), np.asarray(relevances), quantities, ids


def build_model(x,y):
    mlp = Sequential()
    mlp.add(Dense(units=64, activation="relu"))
    mlp.add(Dense(units=1, activation='sigmoid'))
    mlp.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"], validation_split=0.2)
    mlp.fit(x, y, epochs=100, batch_size=32)

    return mlp


def predict_relevances(model, x, quantities, ids):
    predictions = model.predict(x)

    relevances = {}

    for id, quantity, prediction in zip(ids, quantities, predictions):
        if id not in relevances.keys():
            relevances[id] = {quantity: prediction[0]}
        else:
            relevances[id][quantity] = prediction[0]

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
    x, y, quantities, ids = preprocess('dummy_table_relevance.csv')
    mlp = build_model(x, y)
    preds = mlp.predict(x)
    acc_string, acc_number = accuracy(preds, y)
    print(acc_string)
    print(acc_number)
    rel_dict = predict_relevances(mlp, x, quantities, ids)
    mlp.save('relevance_mlp.h5')
    print(rel_dict)

