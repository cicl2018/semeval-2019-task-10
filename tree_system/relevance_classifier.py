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
    quantities_feature = []
    quantities = []
    relevances = []

    #fill the column arrays with corresponding values
    for row in csvreader:
        feature1.append([row['Feature1']])
        feature2.append([row['Feature2']])
        quantities_feature.append([row['Quantity']])
        quantities.append(row['Quantity'])
        relevances.append(row['Relevance'])

    #transform the features to onehot
    feature1_enc = OneHotEncoder(sparse=False)
    feature2_enc = OneHotEncoder(sparse=False)
    quantities_feature_enc = OneHotEncoder(sparse=False, categories='auto')

    feature1_enc.fit(feature1)
    feature2_enc.fit(feature2)
    quantities_feature_enc.fit(quantities_feature)

    feature1 = feature1_enc.transform(feature1)
    feature2 = feature1_enc.transform(feature2)
    quantities_feature = quantities_feature_enc.transform(quantities_feature)

    x = []

    for items in zip(feature1, feature2, quantities_feature):
        row = np.concatenate(items, axis=0)
        x.append(row)

    return np.asarray(x), np.asarray(relevances), np.asarray(quantities)



if __name__ == "__main__":
    x, y, quantities = preprocess('dummy_table_relevance.csv')

    print(x.shape)
    print(x)
    mlp = Sequential()
    mlp.add(Dense(units=64, activation="relu"))
    mlp.add(Dense(units=1, activation='sigmoid'))
    mlp.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"], validation_split=0.2)
    mlp.fit(x, y, epochs=100, batch_size=32)

    preds = mlp.predict(x)

    print(preds)

