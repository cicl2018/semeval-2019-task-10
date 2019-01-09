import numpy as np
from keras import layers
from keras.layers import LSTM, Embedding
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences


class OutputChars:
    """
    Decode our output from one-hot vector to numbers
    """
    def __init__(self, chars):
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    def encode(self, s, num_rows):
        x = np.zeros((num_rows, len(self.chars)))
        for i, c in enumerate(s):
            x[i, self.char_indices[c]] = 1
        return x

    def decode(self, x, calc_argmax=True):
        if calc_argmax:
            x = x.argmax(axis=-1)
        return ''.join(self.indices_char[x] for x in x)


class InputChars:
    """
    Encode input string into vectors
    """
    def __init__(self, chars):
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    def encode(self, s):
        return [self.to_index(c) for c in s]

    def to_index(self, c):
        return self.char_indices[c] + 1


class Colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'


def random_num(digits=3):
    """

    :param digits:
    :return: a random number given digit
    """
    return int(''.join(np.random.choice(list('0123456789')) for i in range(np.random.randint(1, digits + 1))))


def random_variable(choices):
    """

    :param choices:
    :return: a choices
    """
    return np.random.choice(choices)


TRAINING_SIZE = 50000
DIGITS = 3
REVERSE = True
DOUBLE = True


"""
Create our input and outpur chars
"""
input_chars = '0123456789+-=, ?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
input_table = InputChars(input_chars)
output_chars = '0123456789- '
output_table = OutputChars(output_chars)

questions = []
answers = []
seen = set()


"""
generate our datasets
"""
print('Generating data...')
while len(questions) < TRAINING_SIZE:
    a, b = random_num(DIGITS), random_num(DIGITS)
    c = random_variable(list('xyz'))

    key = a, b, c
    if key in seen:
        continue
    seen.add(key)

    ques = 'If {} + {} = {}, what is the value of {}?'.format(c, a, b, c)
    ans = str(b - a)

    if REVERSE:
        ques = ques[::-1]

    if DOUBLE:
        ques += ques;

    questions.append(ques)
    answers.append(ans)


"""
A quick view of our datasets
"""
print('Quick View on Data...')
ques_view = questions[::5]
ans_view = answers[::5]

for i in range(5):
    print("Question: ", ques_view[i], "Answer: ", ans_view[i])

MAX_LENGTH_Q = max([len(str(i)) for i in questions]) * 2
MAX_LENGTH_A = max([len(str(i)) for i in answers])

print("Question Length: ", MAX_LENGTH_Q)
print("Answer Length: ", MAX_LENGTH_A)

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


"""
We shuffle the datasets
"""
indices = np.arange(len(y))
np.random.shuffle(indices)
x = x[indices]
y = y[indices]


"""
cut 5% of our datasets as test data
"""
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

for iteration in range(1, 50):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=1,
              validation_data=(x_val, y_val))
    # Select 10 samples from the validation set at random so we can visualize
    # errors.
    for i in range(10):
        ind = np.random.randint(0, len(x_val))
        rowx, rowy = x_val[np.array([ind])], y_val[np.array([ind])]
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



