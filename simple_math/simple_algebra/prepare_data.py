import numpy as np
import json
from encode import InputChars, OutputChars, Colors


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


def create_choices(ans, gap):
    choices = [ans + i*gap for i in range(-2, 3)]
    np.random.shuffle(choices)
    choices_dict = dict()
    choices_dict['A'] = str(choices[0])
    choices_dict['B'] = str(choices[1])
    choices_dict['C'] = str(choices[2])
    choices_dict['D'] = str(choices[3])
    choices_dict['E'] = str(choices[4])
    if choices[0] == ans:
        answer = 'A'
    if choices[1] == ans:
        answer = 'B'
    if choices[2] == ans:
        answer = 'C'
    if choices[3] == ans:
        answer = 'D'
    if choices[4] == ans:
        answer = 'E'

    return choices_dict, answer


if __name__ == '__main__':
    TRAINING_SIZE = 200000
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
    choices = []
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
        ans = b - a

        if REVERSE:
            ques = ques[::-1]

        if DOUBLE:
            ques += ques

        choice_options, choice_ans = create_choices(ans, 1)

        questions.append(ques)
        choices.append(choice_options)
        answers.append(choice_ans)

    dataset = []

    for i in range(0, TRAINING_SIZE):
        data = dict()
        data['question'] = questions[i]
        data['answer'] = answers[i]
        data['choices'] = choices[i]
        dataset.append(data)

    output_json_string = json.dumps(dataset, indent=4)
    with open('train.json', 'w+') as f:
        f.write(output_json_string)


