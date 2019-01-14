
- A little bit mass here

- First, I have trained our model with both actually questions and make-up questions and save the model

- Then, I over trained our model again with only actual questions, where it will fit prefect with train data. Since the model cannot directly learn from sat questions, I believe this is good.

- Then, I test with our dev data, which results in 33% accuracy, which is good I think

- For testing:
1. run split_data.py first to split data into train and dev
2. run train.py to train data
3. run predict.py to see the result of dev data


============================================

- A simple code I found online which can produce numbers form a input string, such as input "123+23" then the output would be "146". I have changed to three numbers additon or changed "+" into "add" or "add" and "minus" at the same time and worked well

- paper is here [Leaning to Execute](https://arxiv.org/pdf/1410.4615.pdf)
- code is [here](https://github.com/wojciechz/learning_to_execute), but it is writen in lua.

- I will try this model with our data. See if it works.


- I have tried this model to our data, but I don't think it is working. See /simple_math/raw.py

- Also, I have tridd this with simple algebra like "If x + 12 = 45, what is the value of x?". It is learning but not so good. I will try to run this with a large dataset and more iteration. See simple_algebra.py