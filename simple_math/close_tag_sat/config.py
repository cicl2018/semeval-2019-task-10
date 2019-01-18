import json
from encode import InputChars, OutputChars

# for training on a GPU change it to 1024
global BATCH_SIZE
BATCH_SIZE = 128
# for length of a question 150, 350 or 650
global MAX_LENGTH_Q
MAX_LENGTH_Q = 150
# for make up data sise
global TRAINING_SIZE
TRAINING_SIZE = 10000
# for train iteration
global TRAIN_ITER
TRAIN_ITER = 2
# for pre train iteration
global PRE_TRAIN_ITER
PRE_TRAIN_ITER = 2

global PRE_TRAIN_MODEL
PRE_TRAIN_MODEL = "pre_trained_model_20_70k_150.h5"

global TRAINED_MODEL
TRAINED_MODEL = "well_trained_model_20_70k_150_20.h5"





# for answer and chars
print('Preparing chars...')
with open('makeup_questions.json') as f:
    data_train = json.load(f)

with open('sat.train.json') as f:
    data_dev = json.load(f)

data_all = data_train + data_dev
global INPUT_CHARS
INPUT_CHARS = sorted(set(str(data_all)))
print('Preparing chars end')

global INPUT_TABLE
INPUT_TABLE = InputChars(INPUT_CHARS)
global OUTPUT_CHARS
OUTPUT_CHARS = "0123456789- [],"
global OUTPUT_TABLE
OUTPUT_TABLE = OutputChars(OUTPUT_CHARS)
global MAX_LENGTH_A
MAX_LENGTH_A = 5
