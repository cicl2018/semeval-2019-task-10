import json
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import numpy as np

from config import INPUT_CHARS, INPUT_TABLE, OUTPUT_CHARS, OUTPUT_TABLE, MAX_LENGTH_Q


def strip_string(s):
    s = str(s).replace("\\", "")
    s = str(s).replace("}", "")
    s = str(s).replace("{", "")
    s = str(s).replace("(", "")
    s = str(s).replace(")", "")
    return s


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
    if 'E' in choice:
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

    if 'E' in choice and min_score > score_e:
        min_score = score_e
        choice = 'E'

    return choice, min_score


with open("sat.test.json", "r") as f:
    dataset = json.load(f)

trained_model = load_model("well_trained_model_40_600k_650_300.h5")

questions = []
choices = []
ids = []
# answers = []

for data in dataset:
    question = data['question']
    question = str(question).replace("\\", "")
    question = question[::-1]
    questions.append(question)

    id = data['id']
    ids.append(id)

    # answer = data["answer"]
    # answers.append(answer)

    if "choices" in data:
        choice_options = data['choices']
        if "A" in choice_options:
            choice_options["A"] = strip_string(choice_options["A"])
        if "B" in choice_options:
            choice_options["B"] = strip_string(choice_options["B"])
        if "C" in choice_options:
            choice_options["C"] = strip_string(choice_options["C"])
        if "D" in choice_options:
            choice_options["D"] = strip_string(choice_options["D"])
        if "E" in choice_options:
            choice_options["E"] = strip_string(choice_options["E"])
    choices.append(choice_options)

unpad_questions = [INPUT_TABLE.encode(i) for i in questions]
x = pad_sequences(unpad_questions, MAX_LENGTH_Q)

x_train = x

output_json = []
match = 0
total = 0

for i in range(len(questions)):
    print(i, "/", len(questions), "=======", match, total, end='\r')

    rowx = x_train[np.array([i])]
    pred = trained_model.predict_classes(rowx, verbose=0)

    guess = OUTPUT_TABLE.decode(pred[0], calc_argmax=False)

    guess_choice, confident = choose_ans(guess, choices[i])

    if confident > 0:
        continue

    output = dict()
    output['id'] = ids[i]
    output['answer'] = guess_choice

    output_json.append(output)

    # if guess_choice == answers[i]:
    #     match += 1
    # total += 1
print("")
print(len(output_json))

with open("confident_answered_questions.json", "w+") as f:
    output_string = json.dumps(output_json, indent=4)
    f.write(output_string)
