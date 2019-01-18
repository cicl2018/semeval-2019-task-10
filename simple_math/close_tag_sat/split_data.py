import json
import numpy as np

with open('pre_process_sat.json', 'r') as f:
    dataset = json.load(f)

np.random.shuffle(dataset)

# split_at = len(dataset) - len(dataset) // 10
split_at = len(dataset)
(x_train, x_dev) = dataset[:split_at], dataset[split_at:]

with open('train.json', 'w+') as f:
    x_train_output = json.dumps(x_train, indent=4)
    f.write(x_train_output)

with open('dev.json', 'w+') as f:
    x_dev_output = json.dumps(x_dev, indent=4)
    f.write(x_dev_output)
