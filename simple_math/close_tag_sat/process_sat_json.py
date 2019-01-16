import json
import re


def is_number(s):
    match = False
    pattern_straight_num = re.compile("^[-]?[0123456789]+$")
    if pattern_straight_num.match(s):
        match = True

    return match


# with open('original_closed_tag.json', 'r') as f:
with open('sat.train.json', 'r') as f:
    dataset = json.load(f)

new_data = []

for data in dataset:
    if 'choices' in data and len(data['question']) < 150:
        answer = data['choices'][data['answer']]
        if is_number(answer):
            new_data.append(data)


new_data_output = json.dumps(new_data, indent=4)

with open('pre_process_sat.json', 'w+') as f:
    f.write(new_data_output)
