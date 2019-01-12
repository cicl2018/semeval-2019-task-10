import numpy as np
import json
from keras import layers
from keras.layers import LSTM, Embedding, Input
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences

class CharacterTable(object):
    """Given a set of characters:
    + Encode them to a one-hot integer representation
    + Decode the one-hot or integer representation to their character output
    + Decode a vector of probabilities to their character output
    """
    def __init__(self, chars):
        """Initialize character table.

        # Arguments
            chars: Characters that can appear in the input.
        """
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    def encode(self, C, num_rows):
        """One-hot encode given string C.

        # Arguments
            C: string, to be encoded.
            num_rows: Number of rows in the returned one-hot encoding. This is
                used to keep the # of rows for each data the same.
        """
        x = np.zeros((num_rows, len(self.chars)))
        for i, c in enumerate(C):
            x[i, self.char_indices[c]] = 1
        return x

    def decode(self, x, calc_argmax=True):
        """Decode the given vector or 2D array to their character output.

        # Arguments
            x: A vector or a 2D array of probabilities or one-hot representations;
                or a vector of character indices (used with `calc_argmax=False`).
            calc_argmax: Whether to find the character index with maximum
                probability, defaults to `True`.
        """
        if calc_argmax:
            x = x.argmax(axis=-1)
        return ''.join(self.indices_char[x] for x in x)

    def to_char(self, n):
        return self.indices_char[n]

    def sequence_to_index(self, C):
        return [self.to_index(i) for i in C]
    
    def to_index(self, c):
        return self.char_indices[c] + 1


class colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'


print('Preparing data...')
with open('train.json') as f:
    data_train = json.load(f)

with open('dev.json') as f:
    data_dev = json.load(f)

data = data_train + data_dev
chars = sorted(set(str(data)))
char_table = CharacterTable(chars)
chars_ans = '0123456789 -.'
char_table_ans = CharacterTable(chars_ans)

def preproces_data(data):
    questions = []
    answers = []
    for item in data:
        if "question" not in item \
        and "answer" not in item \
        and "choices" not in item:
            continue

        len_choices = [len(i) for k, i in item['choices'].items()]
        if max(len_choices) > 3:
            continue

        questions.append(item['question'][::-1])
        answers.append(item['choices'][item['answer']])
    return questions, answers

unpad_questions, unpad_answers = preproces_data(data)

print('Quick look at data:')
for i in range(5):
    print('question: ', unpad_questions[i])
    print('answer: ', unpad_answers[i], '\n')
print('\n')

maxlen_x = max([len(str(i)) for i in unpad_questions])
maxlen_y = max([len(str(i)) for i in unpad_answers])

print("Max length of questions: ", maxlen_x)
print("Max length of answers: ", maxlen_y)

print('\n')

unpad_questions = [char_table.sequence_to_index(i) for i in unpad_questions]

x = pad_sequences(unpad_questions, maxlen_x)
# answers = pad_sequences(unpad_answers, maxlen_y, dtype=np.char)
answers = [i + ' ' * (maxlen_y - len(i)) for i in unpad_answers]

# print('Encoding...')
# x = np.zeros((len(questions), maxlen_x, len(chars)), dtype=np.bool)
y = np.zeros((len(answers), maxlen_y, len(chars_ans)), dtype=np.bool)
# for i, sentence in enumerate(questions):
#     x[i] = char_table.sequence_to_index(sentence)
for i, sentence in enumerate(answers):
    y[i] = char_table_ans.encode(sentence, maxlen_y)

indices = np.arange(len(y))
np.random.shuffle(indices)
x = x[indices]
y = y[indices]

split_at = len(x) - len(x) // 50
(x_train, x_val) = x[:split_at], x[split_at:]
(y_train, y_val) = y[:split_at], y[split_at:]

print('Training Data:')
print(x_train.shape)
print(y_train.shape)

print('Validation Data:')
print(x_val.shape)
print(y_val.shape)

HIDDEN_SIZE = 128
BATCH_SIZE = 128
LAYERS = 1

print('Build model...')
model = Sequential()
model.add(Embedding(input_dim=len(chars) + 1, output_dim=HIDDEN_SIZE, input_length=maxlen_x, mask_zero=True))
model.add(LSTM(HIDDEN_SIZE, input_shape=(maxlen_x, len(chars))))
model.add(layers.RepeatVector(maxlen_y))
for _ in range(LAYERS):
    model.add(LSTM(HIDDEN_SIZE, return_sequences=True))
model.add(layers.TimeDistributed(layers.Dense(len(chars_ans), activation='softmax')))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.summary()

for iteration in range(1, 50):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=10,
              validation_data=(x_val, y_val))
    # Select 10 samples from the validation set at random so we can visualize
    # errors.
    for i in range(10):
        ind = np.random.randint(0, len(x_val))
        rowx, rowy = x_val[np.array([ind])], y_val[np.array([ind])]
        preds = model.predict_classes(rowx, verbose=0)
        # q = char_table.decode(rowx[0])
        correct = char_table_ans.decode(rowy[0])
        guess = char_table_ans.decode(preds[0], calc_argmax=False)
        # print('Q', q, end=' ')
        print('T', correct, end=' ')
        if correct == guess:
            print(colors.ok + '☑' + colors.close, end=' ')
        else:
            print(colors.fail + '☒' + colors.close, end=' ')
        print(guess)
