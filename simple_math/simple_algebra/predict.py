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


trained_model = load_model('simple_model.h5')

questions, answers, choices, correct_choices = process_data('train.json', 100, predict=True)

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

total = 0
matches = 0

# print('Start predicting...')
# preds = trained_model.predict_classes(x_train, verbose=0)
# print('Predicting end')

# for i in range(len(x_train)):
#     # correct = output_table.decode(y_train[0])
#     questions = x_train[i]
#     preds = trained_model.predict_classes(questions, verbose=0)
#
#     correct_ans = answers[i]
#     correct_choice = correct_choices[i]
#     choice = choices[i]
#     guess = output_table.decode(preds[0], calc_argmax=False)
#
#     guess_choice = choose_ans(guess, choice)
#
#     total += 1
#     if guess_choice == correct_choice:
#         matches += 1
#
#     print("correct ans:\t", correct_ans,
#           "\tcorrect_choice:\t", correct_choice,
#           # "\tchoice:\t", choice,
#           "\tguess:\t", guess,
#           "\tguess_choice:\t", guess_choice)
#
# print("Train set exact acc: ", matches / total)

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

