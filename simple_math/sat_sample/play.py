import json

with open('train.json') as f:
    data_train  = json.load(f)

with open('dev.json') as f:
    data_dev = json.load(f)

data = data_train + data_dev
chars = sorted(set(str(data)))



print(len(data), len(data_train), len(data_dev))

print(chars)