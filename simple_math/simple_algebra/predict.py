import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from process_json import *
from encode import Colors

trained_model = load_model('simple_plus_model.h5')

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

total = len(x_train)
matches = 0

preds = trained_model.predict_classes(x_train)

for i in range(len(x_train)):
    correct = output_table.decode(y_train[0])
    guess = output_table.decode(preds[0], calc_argmax=False)
    if correct == guess:
        matches += 1

print("Train set acc: ", matches / total)

# Select 10 samples from the validation set at random so we can visualize
# errors.
for i in range(10):
    ind = np.random.randint(0, len(x_train))
    rowx, rowy = x_train[np.array([ind])], y_train[np.array([ind])]
    preds = trained_model.predict_classes(rowx, verbose=0)
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

