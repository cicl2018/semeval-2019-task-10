import json
from encode import InputChars, OutputChars

input_chars = '0123456789+-=, ?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
input_table = InputChars(input_chars)
output_chars = '0123456789- '
output_table = OutputChars(output_chars)
MAX_LENGTH_Q = 550
MAX_LENGTH_A = 5
DOUBLE = True
REVERSE = True


def process_data(file):
    with open(file, 'r') as f:
        dataset = json.load(f)

    questions = []
    answers = []

    for data in dataset:
        question = data['question']
        if DOUBLE:
            question = question + question + question + question
        if REVERSE:
            question = question[::-1]
        questions.append(question)
        answers.append(data['choices'][data['answer']])

    return questions, answers
