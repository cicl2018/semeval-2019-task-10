import json
import re

train, dev = [], []

with open('../data_analysis/sat.train.json') as json_file:
    data = json.load(json_file)

    for i in range(0, len(data)):
        if i < 4 / 5 * len(data) - 1:
            train.append(data[i])
        else:
            dev.append(data[i])


with open('train.json', 'w') as output:
    json.dump(train, output, indent= 4)

with open('dev.json', 'w') as output:
    json.dump(dev, output, indent= 4)