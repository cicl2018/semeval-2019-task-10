import json
import re
import numpy as np
import keras
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Embedding, SimpleRNN, GRU, LSTM, Input


def preprocess_train(filepath):
    strings = []
    train_x, train_choices, train_y = [], [], []

    vocab = {'unknown': 1}
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
                    train_choices.append(item['choices'][choice])
                else:
                    train_choices.append(np.random.randint(0, 100))
                if item['choices'][choice] == answer:
                    train_y.append(1)
                else:
                    train_y.append(0)

    for item in strings:
        currentRow = []
        for char in item:
            if char not in vocab.keys():
                vocab[char] = charInt
                charInt += 1
            currentRow.append(vocab[char])
        train_x.append(currentRow)

    return train_x, np.asarray(train_y), np.asarray(train_choices), vocab, len(data)


def preprocess_test(filepath, vocab):
        strings = []
        test_x, test_choices, test_y = [], [], []
        vocab = vocab

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
                        test_choices.append(item['choices'][choice])
                    else:
                        test_choices.append(np.random.randint(0, 100))
                    if item['choices'][choice] == answer:
                        test_y.append(1)
                    else:
                        test_y.append(0)

        for item in strings:
            currentRow = []
            for char in item:
                if char not in vocab.keys():
                    currentRow.append(vocab['unknown'])
                else:
                    currentRow.append(vocab[char])
            test_x.append(currentRow)

        return test_x, np.asarray(test_y), np.asarray(test_choices), len(data)


def acc(predictions, results, gold, length):
    current_question = results[0]
    options = []
    matches = 0

    for prediction, question in zip(predictions, results):
        if np.array_equal(question, current_question):
            options.append(float(prediction))
        else:
            answer = (max(options))
            if gold[predictions.tolist().index([answer])] == 1:
                matches += 1
            options = []
            current_question = question
            options.append(float(prediction))

    answer = (max(options))
    if gold[predictions.tolist().index([answer])] == 1:
        matches += 1

    print(matches, "/", length)
    return matches / length


if __name__ == '__main__':
    train_x_unpadded, train_y, train_choices, vocab, train_set_length = preprocess_train('train.json')

    test_x_unpadded, test_y, test_choices, test_set_length = preprocess_test('dev.json', vocab)

    train_x = pad_sequences(train_x_unpadded)
    test_x = pad_sequences(test_x_unpadded, maxlen=len(train_x[0]))

    questions_input = Input(shape=(len(train_x[0]),))
    choices_input = Input(shape=(1,))
    choices_m = Dense(32, activation='relu')(choices_input)

    x = Embedding(input_dim=len(vocab) + 1, output_dim=64, input_length=len(train_x[0]))(questions_input)
    x = GRU(64)(x)
    #x = keras.layers.concatenate([x, choices_m], axis=1)
    #x = Dense(64, activation='relu')(x)
    #x = Dense(64, activation='relu')(x)
    #x = Dense(64, activation='relu')(x)
    #x = Dense(64, activation='relu')(x)
    x = Dense(32, activation='linear')(x)

    output = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=[questions_input, choices_input], outputs=output)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit([train_x, train_choices], train_y, epochs=10, batch_size=32)

    test_predictions = model.predict([test_x, test_choices])
    print('Accuracy on the test set:', acc(test_predictions, test_x, test_y, test_set_length))

    train_predictions = model.predict([train_x, train_choices])
    print('Accuracy on the training set:', acc(train_predictions, train_x, train_y, train_set_length))
