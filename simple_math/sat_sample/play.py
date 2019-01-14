import json

with open('train.json') as f:
    data_train = json.load(f)

max = 0
max_1 = 0
max_2 = 0

print(len(data_train))
for data in data_train:
    if len(data['question']) > max:
        max_3 = max_2
        max_2 = max_1
        max_1 = max
        max = len(data['question'])
        print('\n')
        print(data['question'])


print(max, max_1, max_2, max_3)
