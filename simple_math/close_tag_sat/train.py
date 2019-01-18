import numpy as np
from keras import layers
from keras.layers import LSTM, Embedding
from keras.models import Sequential, load_model
from keras.preprocessing.sequence import pad_sequences
import json
from process_json_data import *
from encode import *


questions_train = []
answers_train = []

"""
process data from dataset
"""
print("loading data...")
# questions, answers = process_data('train.json', double=True, reverse=True)
#
# questions_train += questions
# answers_train += answers

questions, answers = process_data('train.json', double=False, reverse=True)

questions_train += questions
answers_train += answers

"""
Transfrom questions into vectors and pad_them
"""
unpad_questions = [input_table.encode(i) for i in questions_train]
x = pad_sequences(unpad_questions, MAX_LENGTH_Q)

"""
Encode the answer in to one-hot vectors
"""
pad_answers = [i + ' ' * (MAX_LENGTH_A - len(i)) for i in answers_train]
y = np.zeros((len(answers_train), MAX_LENGTH_A, len(output_chars)), dtype=np.bool)
for i, sentence in enumerate(answers_train):
    y[i] = output_table.encode(sentence, MAX_LENGTH_A)

x_train = x
y_train = y


HIDDEN_SIZE = 128
BATCH_SIZE = 1024
LAYERS = 1

print('Load model...')

model = load_model("pre_trained_model_40_600k_650.h5")

for iteration in range(1, 40):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=20)

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


model.save('well_trained_model_40_600k_650_40.h5')



