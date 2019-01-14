import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from process_json import *
from encode import Colors


def score_ans(cal_answer, target_ans):
    score = 0
    len_a = len(cal_answer)
    len_b = len(target_ans)
    if len_a < len_b:
        shorter_len = len_a
    else:
        shorter_len = len_b

    for i in range(0, shorter_len):
        char_a = cal_answer[i]
        char_b = target_ans[i]

        if char_a != char_b:
            score += shorter_len - i

    return score


def choose_ans(cal_answer, choice):
    score_a = score_ans(cal_answer, choice['A'])
    score_b = score_ans(cal_answer, choice['B'])
    score_c = score_ans(cal_answer, choice['C'])
    score_d = score_ans(cal_answer, choice['D'])
    score_e = score_ans(cal_answer, choice['E'])

    min_score, choice = score_a, 'A'

    if min_score > score_b:
        min_score = score_b
        choice = 'B'

    if min_score > score_c:
        min_score = score_c
        choice = 'C'

    if min_score > score_d:
        min_score = score_d
        choice = 'D'

    if min_score > score_e:
        min_score = score_e
        choice = 'E'

    return choice


trained_model = load_model('simple_plus_model.h5')

questions_train = []
answers_train = []

"""
process data from dataset
"""
print("loading data...")
questions, answers, choices, correct_choices = process_data('short_tag.json', predict=True, double=False, reverse=True)

questions_train += questions
answers_train += answers

# questions, answers = process_data('short_tag.json', double=False, reverse=False)
#
# questions_train += questions
# answers_train += answers

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

total = 0
match = 0

for i in range(len(x_train)):
    rowx, rowy = x_train[np.array([i])], y_train[np.array([i])]
    preds = trained_model.predict_classes(rowx, verbose=0)
    # q = char_table.decode(rowx[0])
    # Questions
    question = questions[i]
    question = question[::-1]

    # Choices for question
    choice_options = choices[i]

    # Correct sequence answer for question
    correct = output_table.decode(rowy[0])

    # Correct choice answer for question
    correct_choice = correct_choices[i]

    # Out guess for sequence ans
    guess = output_table.decode(preds[0], calc_argmax=False)

    #Our guess for choice
    guess_choice = choose_ans(guess, choice_options)

    # print('Q', question, end=' ')
    print('T', correct, end=' ')
    if correct == guess:
        print(Colors.ok + '☑' + Colors.close, end=' ')
    else:
        print(Colors.fail + '☒' + Colors.close, end=' ')
    print(guess)

    if guess_choice == correct_choice:
        match += 1
    total += 1

print("Training data acc: ", match/total)
