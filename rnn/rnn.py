import json
import re
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, SimpleRNN, TimeDistributed, GRU, LSTM
from sklearn.metrics import accuracy_score


def preprocess(filepath):
    strings = []
    answers = []

    vocab = {"unknown": 1}
    wordInt = 2
    with open(filepath) as json_file:
        data = json.load(json_file)

        for item in data:
            if 'choices' not in item.keys():
                continue
            answer_key = item['answer']
            answer = item['choices'][answer_key]

            if not re.match(r'^(([0-9]*)|(([0-9]*)\.([0-9]*)))$', answer):
                continue

            strings.append(item['question'])
            answers.append(answer)

    training_strings, test_strings, training_answers, test_answers = [], [], [], []

    for i in range(0, len(strings)):
        if i < 4 / 5 * len(strings):
            training_strings.append(strings[i])
            training_answers.append(answers[i])
        else:
            test_strings.append(strings[i])
            test_answers.append(answers[i])

    training_vectors = []
    test_vectors = []

    for item in training_strings:
        words = item.split(" ")
        currentRow = []
        for item2 in words:
            if item2 not in vocab.keys():
                vocab[item2] = wordInt
                wordInt += 1
            currentRow.append(vocab[item2])
        training_vectors.append(currentRow)

    for item in test_strings:
        words = item.split(" ")
        currentRow = []
        for item2 in words:
            if item2 not in vocab.keys():
                currentRow.append(vocab['unknown'])
            else:
                currentRow.append(vocab[item2])
        test_vectors.append(currentRow)


    return training_vectors, np.asarray(training_answers), test_vectors, np.asarray(test_answers), vocab


def to_onehot(array):
    array_onehot_buffer = to_categorical(array)

    array_onehot = []
    for row in array_onehot_buffer:
        array_onehot.append(row.flatten())

    return np.asarray(array_onehot)

if __name__ == "__main__":
    training_vectors_unpadded, training_answers, test_vectors_unpadded, test_answers, vocab = preprocess('../data/sat.train.json')

    training_vectors = pad_sequences(training_vectors_unpadded)
    test_vectors = pad_sequences(test_vectors_unpadded)
    test_vectors = test_vectors[:, 6:]

    #training_vectors = to_onehot(training_vectors)
    #test_vectors = to_onehot(test_vectors)
    """
    rnn = Sequential((Embedding(len(vocab), 32, mask_zero=True, input_length= len(training_vectors[0])),
                      Dropout(0.5),
                      SimpleRNN(64, return_sequences=True),
                      Dropout(0.5),
                      TimeDistributed(Dense(len(vocab), activation='softmax'))
                      ))

    rnn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    rnn.fit(training_vectors, training_answers, epochs = 5, batch_size=32)

    predictions = rnn.predict(test_vectors)
    """
    rnn = Sequential()
    rnn.add(Embedding(input_dim=len(vocab) + 1, output_dim=64, input_length=len(training_vectors[0])))
    rnn.add(Dropout(0.5))
    rnn.add(SimpleRNN(units=64))
    rnn.add(Dense(1, activation="linear"))
    rnn.compile(loss="mean_absolute_error", optimizer="adam", metrics=['accuracy'])
    rnn.fit(training_vectors, training_answers, epochs=40, batch_size=32)

    predictions_raw = rnn.predict(test_vectors)

    matches = 0

    predictions = []
    for entry in predictions_raw:
        for entry2 in entry:
            predictions.append(int(round(entry2)))

    print(test_answers)
    print(predictions)
    for prediction, answer in zip(predictions, test_answers):
        if str(prediction) == answer:
            matches += 1

    print(matches)