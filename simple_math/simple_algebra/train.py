import numpy as np
from keras import layers
from keras.layers import LSTM, Embedding
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
import json
from process_json import *
from encode import *


"""
process data from dataset
"""
with open('train.json', 'r') as f:
    dataset_train = json.load(f)

questions, answers = process_data('train.json')

"""
Transfrom questions into vectors and pad_them
"""
unpad_questions = [input_table.encode(i) for i in questions]
x = pad_sequences(unpad_questions, MAX_LENGTH_Q)

"""
Encode the answer in to one-hot vectors
"""
pad_answers = [i + ' ' * (MAX_LENGTH_A - len(i)) for i in answers]
y = np.zeros((len(answers), MAX_LENGTH_A, len(output_chars)), dtype=np.bool)
for i, sentence in enumerate(answers):
    y[i] = output_table.encode(sentence, MAX_LENGTH_A)

x_train = x
y_train = y

HIDDEN_SIZE = 512
BATCH_SIZE = 512
LAYERS = 1

print('Build model...')
model = Sequential()
model.add(Embedding(input_dim=len(input_chars) + 1, output_dim=HIDDEN_SIZE, input_length=MAX_LENGTH_Q, mask_zero=True))
model.add(LSTM(HIDDEN_SIZE, input_shape=(MAX_LENGTH_Q, len(input_chars))))
model.add(layers.RepeatVector(MAX_LENGTH_A))
for _ in range(LAYERS):
    model.add(LSTM(HIDDEN_SIZE, return_sequences=True))
model.add(layers.TimeDistributed(layers.Dense(len(output_chars), activation='softmax')))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.summary()

for iteration in range(1, 30):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=1)

    # Select 10 samples from the validation set at random so we can visualize
    # errors.
    for i in range(10):
        ind = np.random.randint(0, len(x_train))
        rowx, rowy = x_train[np.array([ind])], y_train[np.array([ind])]
        preds = model.predict_classes(rowx, verbose=0)
        # q = char_table.decode(rowx[0])
        correct = output_table.decode(rowy[0])
        guess = output_table.decode(preds[0], calc_argmax=False)
        # print('Q', q, end=' ')
        print('T', correct, end=' ')
        if correct == guess:
            print(Colors.ok + '☑' + Colors.close, end=' ')
        else:
            print(Colors.fail + '☒' + Colors.close, end=' ')
        print(guess)


model.save('simple_plus_model.h5')



