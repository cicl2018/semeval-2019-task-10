import json
from encode import InputChars, OutputChars

print('Preparing chars...')
with open('makeup_questions.json') as f:
    data_train = json.load(f)

with open('sat.train.json') as f:
    data_dev = json.load(f)

data_all = data_train + data_dev
input_chars = sorted(set(str(data_all)))
print('Preparing chars end')

input_table = InputChars(input_chars)
output_chars = "0123456789- [],"
output_table = OutputChars(output_chars)
MAX_LENGTH_Q = 150
MAX_LENGTH_A = 5


def process_data(file, size=0, predict=False, double=True, reverse=True):
    with open(file, 'r') as f:
        dataset = json.load(f)

    if predict:
        questions = []
        answers = []
        choices = []
        correct_choices = []

        for data in dataset:
            question = data['question']
            question = str(question).replace("\\", "")
            if double:
                question = question + question
            if reverse:
                question = question[::-1]
            questions.append(question)

            answer = data['choices'][data['answer']]
            answers.append(answer)

            correct_choice = data['answer']
            correct_choices.append(correct_choice)

            choice = data['choices']
            choices.append(choice)

        if size != 0:
            questions = questions[:size]
            answers = answers[:size]
            choices = choices[:size]
            correct_choices = correct_choices[:size]

        return questions, answers, choices, correct_choices

    questions = []
    answers = []

    for data in dataset:
        question = data['question']
        question = str(question).replace("\\", "")
        if double:
            question = question + question
        if reverse:
            question = question[::-1]
        questions.append(question)
        answer = data['choices'][data['answer']]
        answer = str(answer).replace("\\", "")
        answers.append(answer)

    if size != 0:
        questions = questions[::size]
        answers = answers[::size]

    return questions, answers


def process_chars(char_list):
    chars = set()
    for data in char_list:
        chars.union(set(data))

    return chars

