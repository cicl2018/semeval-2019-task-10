import json
import re
import numpy as np
import keras
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Embedding, SimpleRNN, TimeDistributed, GRU, LSTM, Concatenate, Input
from sklearn.metrics import accuracy_score


def preprocess(filepath):
    strings = []
    available_choices = []
    is_correct_answer = []

    vocab = {"unknown": 1}
    charInt = 2
    with open(filepath) as json_file:
        data = json.load(json_file)

        for item in data:
            if 'choices' not in item.keys():
                continue
            answer_key = item['answer']
            answer = item['choices'][answer_key]

            if not re.match(r'^((-*)([0-9]*)|((-*)([0-9]*)\.([0-9]*)))$', answer):
                continue

            for choice in item['choices']:
                strings.append(item['question'])
                if re.match(r'^((-*)([0-9]*)|(([0-9]*)\.([0-9]*)))$', item['choices'][choice]):
                    available_choices.append(item['choices'][choice])
                else:
                    available_choices.append(np.random.randint(0, 100))
                if item['choices'][choice] == answer:
                    is_correct_answer.append(1)
                else:
                    is_correct_answer.append(0)


    training_strings, test_strings, train_choices, test_choices, train_y, test_y = [], [], [], [], [], []

    for i in range(0, len(strings)):
        if i < 4 / 5 * len(strings):
            training_strings.append(strings[i])
            train_y.append(is_correct_answer[i])
            train_choices.append(available_choices[i])
        else:
            test_strings.append(strings[i])
            test_y.append(is_correct_answer[i])
            test_choices.append(available_choices[i])


    train_x = []
    test_x = []

    for item in training_strings:
        currentRow = []
        for char in item:
            if char not in vocab.keys():
                vocab[char] = charInt
                charInt += 1
            currentRow.append(vocab[char])
        train_x.append(currentRow)

    for item in test_strings:
        currentRow = []
        for char in item:
            if char not in vocab.keys():
                currentRow.append(vocab["unknown"])
            else:
                currentRow.append(vocab[char])
        test_x.append(currentRow)


    return train_x, np.asarray(train_y), np.asarray(train_choices), test_x, np.asarray(test_y), np.asarray(test_choices), vocab


def to_onehot(array):
    array_onehot_buffer = to_categorical(array)

    array_onehot = []
    for row in array_onehot_buffer:
        array_onehot.append(row.flatten())

    return np.asarray(array_onehot)

if __name__ == "__main__":
    train_x_unpadded, train_y, train_choices, test_x_unpadded, test_y, test_choices, vocab = preprocess('../data/sat.train.json')

    train_x = pad_sequences(train_x_unpadded)
    test_x = pad_sequences(test_x_unpadded, maxlen= len(train_x[0]))

    for item in train_choices:
        print(item)

    #training_vectors = to_onehot(training_vectors)
    #test_vectors = to_onehot(test_vectors)

    questions_input = Input(shape=(len(train_x[0]),))
    x = Embedding(input_dim=len(vocab) + 1, output_dim=64, input_length=len(train_x[0]))(questions_input)
    #questions_dense = Dense(2,)(questions_input)
    choices_input = Input(shape=(1,))
   # questions_dense = Dense(2, )(choices_input)
    x = keras.layers.concatenate([x, choices_input], axis=1)
    x = GRU(64)(x)

    #x = keras.layers.concatenate([x, choices_input], axis=1)
    output = Dense(1, activation="softmax")(x)

    model = Model(inputs=[questions_input, choices_input], outputs=output)
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
    model.fit([train_x, train_choices], train_y, epochs=20, batch_size=32)

    predictions = model.predict([test_x, test_choices])

    matches = 0

    print(test_y)
    print(predictions)
    for prediction, answer in zip(predictions, test_y):
        if prediction == answer:
            matches += 1

    print(matches)
    #questions_input.add(Embedding(input_dim=len(vocab) + 1, output_dim=64, input_length=len(train_x[0])))(train_x)
    """
    rnn.add(Dropout(0.5))
    rnn.add(SimpleRNN(units=64))
    rnn.add(Dense(2, activation="softmax"))
    rnn.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
    rnn.fit(train_x, train_y, epochs=20, batch_size=32)

    predictions = rnn.predict(test_x)

    matches = 0
    
    print(test_y)
    print(predictions)
    for prediction, answer in zip(predictions, test_y):
        if prediction == answer:
            matches += 1

    print(matches)
"""