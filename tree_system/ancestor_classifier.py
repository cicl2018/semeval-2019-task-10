from keras.layers import Dense, Dropout
from keras.utils import to_categorical
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
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
    operations = []

    #fill the column arrays with corresponding values
    for row in csvreader:
        feature1.append([row['Feature1']])
        feature2.append([row['Feature2']])
        quantity1.append([row['Quantity1']])
        quantity2.append([row['Quantity1']])
        quantities.append((row['Quantity1'], row['Quantity2']))
        operations.append([row['Operation']])

    #transform the features to onehot
    feature1_enc = OneHotEncoder(sparse=False)
    feature2_enc = OneHotEncoder(sparse=False)
    quantity1_enc = OneHotEncoder(sparse=False, categories='auto')
    quantity2_enc = OneHotEncoder(sparse=False, categories='auto')

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

    return np.asarray(x), operations, quantities



if __name__ == "__main__":
    x, y, quantities = preprocess('dummy_table_ancestor.csv')

    y_enc = OneHotEncoder(sparse=False)
    y_enc.fit(y)
    y = y_enc.transform(y)

    mlp = Sequential()
    mlp.add(Dense(units=64, activation="relu"))
    mlp.add(Dense(units=3, activation='softmax'))
    mlp.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"], validation_split=0.2)
    mlp.fit(x, y, epochs=100, batch_size=32)

    preds = mlp.predict(x)
    preds = np.round_(preds)
    preds = y_enc.inverse_transform(preds)

    answers = y_enc.inverse_transform(y)

    matches = 0
    for prediction, answer in zip(preds, answers):
        if prediction == answer:
            matches += 1
    print(matches, '/', len(y))
    print(np.round(matches / len(y), decimals=4))


