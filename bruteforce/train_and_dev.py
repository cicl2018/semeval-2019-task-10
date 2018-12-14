import json
import re

numeric = []

with open('../data/sat.train.json') as json_file:
    data = json.load(json_file)

    for item in data:
        if 'choices' not in item.keys():
            continue
        answer_key = item['answer']
        answer = item['choices'][answer_key]

        if not re.match(r'^((-*)([0-9]*)|((-*)([0-9]*)\.([0-9]*)))$', answer):
            continue

        numeric.append(item)

numeric_train = []
numeric_dev = []

for i in range(0, len(numeric)):
    if i < 4 / 5 * len(numeric) - 1:
        numeric_train.append(numeric[i])
    else:
        numeric_dev.append(numeric[i])

with open('train.json', 'w') as output:
    json.dump(numeric_train, output, indent= 4)

with open('dev.json', 'w') as output:
    json.dump(numeric_dev, output, indent= 4)