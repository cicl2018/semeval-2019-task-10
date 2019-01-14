
#### A cleaned up version is in close_tag_sat

##### Libraries:
1. encode.py: encode and decode sequence to vec
2. process_json_data.py: pre-process data in json into list

- A full reproduction is as follow:
1. First generate make-up questions, using prepare_data.py. makeup_questios.json will generate.
2. Pre-train the model with pre_train.py, where it will train the model with makeup questions, and save model in pre_trained_model.h5
3. Pre-process original sat questions, which resulting only numeric answer question and questions no longer than 150 characters
4. Split sat into train and dev by split_data.py, which will generate train.json and dev.json
5. Train model with sat questions a lot, by train.py, which saves to well_trained_model.h5
6. Run predict.py to see the result
7. Repeat 4 to 6 for small testing




============================================

- A simple code I found online which can produce numbers form a input string, such as input "123+23" then the output would be "146". I have changed to three numbers additon or changed "+" into "add" or "add" and "minus" at the same time and worked well

- paper is here [Leaning to Execute](https://arxiv.org/pdf/1410.4615.pdf)
- code is [here](https://github.com/wojciechz/learning_to_execute), but it is writen in lua.

- I will try this model with our data. See if it works.


- I have tried this model to our data, but I don't think it is working. See /simple_math/raw.py

- Also, I have tridd this with simple algebra like "If x + 12 = 45, what is the value of x?". It is learning but not so good. I will try to run this with a large dataset and more iteration. See simple_algebra.py