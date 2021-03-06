## Features

[Features](./features/features.md)

## Statistics

- Questions with glf json file are in data_analysis

- ==============================
- Data Analysis
- ==============================
- ==============================
- Total Questions: 2224
- ==============================
- Open Questions: 318
- Close Questions: 846 (425 with logical forms, 421 without logical forms)
- Geometry Questions: 593
- Other Questions: 70
- ==============================
- Numerical Answer Questions: 815
- Not Numerical Answer Questions: 1409
- ==============================
- Diagram Questions: 642
- Not a Diagram Questions: 1582
- Geometry but Not a Diagram Questions: 186
- Have Diagram but Not a Geometry Questions: 235
- ==============================

- Right now, numerical Answer Question only show exact numerical answers.
- Files are in the data_analysis folder.

## Latex Parser
- Majority of Latex parsers are dealing with document, sections and subsections. However, I do find one [latex2sympy](https://github.com/augustt198/latex2sympy) that may be useful to us. It converts latex math expressions into sympy. I haven't look deep into it yet.


## Reading list
- Surveys:
  - [A Survey of Question Answering for Math and Science Problem](https://arxiv.org/pdf/1705.04530.pdf)
  - [The Gap of Semantic Parsing: A Survey on Automatic Math Word Problem Solvers](https://arxiv.org/pdf/1808.07290.pdf)
- SigmaDolphin Project:
  - [Automatically Solving Number Word Problems by Semantic Parsing and Reasoning](http://aclweb.org/anthology/D15-1135)
  - [How Well Do Computers Solve Math Word Problems?](http://www.aclweb.org/anthology/P16-1084)
- Euclid Project:
  - [Beyond Sentential Semantic Parsing: Tackling the Math SAT with a Cascade of Tree Transducers](https://pdfs.semanticscholar.org/c22a/240d1087603664826e9aab809273ed9bff15.pdf?_ga=2.52187753.1130679049.1530133172-566539276.1446829155&_gac=1.6555398.1527028246.EAIaIQobChMI9YuywK-a2wIVlcBkCh0WKw_kEAAYASAAEgKwgPD_BwE)
  - [Interactive Visualization for Linguistic Structure](http://ai2-website.s3.amazonaws.com/publications/InteractiveVisualizationOfLinguisticStructure.pdf)
  - [Solving Geometry Problems: Combining Text and Diagram Interpretation](https://pdfs.semanticscholar.org/c87d/ccf7c21e67679389f23f86f039cd96720c3f.pdf?_ga=2.154008190.797290392.1543428819-2132294497.1543428819)
- ALGES Project:
  - [Parsing Algebraic Word Problems into Equations](https://homes.cs.washington.edu/~hannaneh/papers/algebra.pdf)
- Other:
  - [A Question Answer System for Math Word Problems](https://www.google.de/search?q=A+Question+Answer+System+for+Math+Word+Problems&rlz=1C1CHBF_deDE823DE823&oq=A+Question+Answer+System+for+Math+Word+Problems&aqs=chrome..69i57j69i60.584j0j7&sourceid=chrome&ie=UTF-8#cns=0)
  - [MathDQN: Solving Arithmetic Word Problems via Deep Reinforcement Learning](https://aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/16749)
  
## Links
### Euclid Project
- [Start page](https://allenai.org/euclid/)
- GeoS - End-to-End Geometry Problem Solver
  - [Start page of GeoS](http://geometry.allenai.org)
  - [GitHub repository of GeoS](https://github.com/uwnlp/geosolver)
- Hierplane - an open-source Javascript library for visualizing and exploring trees
  - [Start page of Hierplane](https://allenai.github.io/hierplane/)
  - [GitHub repository of Hierplane](https://github.com/allenai/hierplane)
### ALGES Project
- [Repository](https://gitlab.cs.washington.edu/ALGES/TACL2015)

## Notes
#### 13.12.2018
- a good idea to get logical forms both from closed-algebra and open-algebra questions
- Parsers to try: UDPipe > Henry, different kinds of Stanford parser (esp. neural network based one) > Alina, maybe some other parsers?
- Deep reinforcement learning (in the paper about MathDQN) is about giving feedback in the end to the whole tree
- data augmentation may be useful (makes sense for the questions that have logical forms), but first we should get some meaningful results
- ways to run neural network: 
  - no preprocessing > Jonas
  - assertion extraction (formulas) - ?
  - simple linguistic processing like segmentation - ?
  - UDPipe (develop features for parsed sequences manually; come up with a lot of features, the system should decide if they are important or not)
- if running NN on simple strings (without preprocessing), develop features for non-preprocessed sequences: neighboring words etc. > Henry, Alina
- problem for the approach in the paper about MathDQN - questions are very simple comparing to our dataset
- Q-learning > Alina (for entity extraction)
- check discussion in the group
- (Python) library for parsing Latex expressions > Henry


#### 29.11.2018
- Might make sense to parse strings with Latex
- Check the email list/ some other kind of discussions in the project
- Our MAIN GOAL is probably improving getting logical forms
- We should run the programs available and analyze failures (Euklid > Alina, ALGES > Henry)
- Modify the RNN > Jonas

#### 22.11.2018
- Get statistics of the training data > Henry
- Try to use machine learning for:
  1. raw strings and answers (some sort of numeric prediction) > Jonas
  2. raw strings and logical forms 
- Papers and systems available so far > Alina
- As we might need more data for a statistical approach, the existing data can be extended half-manually

#### 14.11.2018
- statistical approach
- semantic representations
- it's not necessary to deal with all the types of questions, it's better to start with Closed-vocabulary algebra and Open-vocabulary algebra types
- if we don't have time for image processing, we can ignore this type of questions or try to come up with a program that would be a bit better than a simple guesser

# SemEval 2019, Task 10: Math Question Answering

### Organizers

Mark Hopkins (Reed College), Ronan Le Bras (Allen Institute for Artificial Intelligence), Cristian Petrescu-Prahova, Gabriel Stanovsky (Allen Institute for Artificial Intelligence), Hannaneh Hajishirzi (University of Washington), Rik Koncel-Kedziorski (University of Washington)

### Mailing List
semeval-2019-task-10@googlegroups.com 

### Key Dates
- 10 Jan 2019: Evaluation start
- 24 Jan 2019: Evaluation end
- 05 Feb 2019: Results posted
- 28 Feb 2019: System and Task description paper submissions due by 23:59 GMT -12:00
- 14 Mar 2019: Paper reviews due (for both systems and tasks)
- 06 Apr 2019: Author notifications
- 20 Apr 2019: Camera ready submissions due
- Summer 2019: SemEval 2019

### Quickstart
Go [here](https://github.com/allenai/semeval-2019-task-10/blob/master/docs/gettingStarted.md) to get started.

### The CodaLab competition page

[https://competitions.codalab.org/competitions/20013]

### Task Overview

Over the past four years, there has been a surge of interest in math question answering. In this SemEval task, we provide the opportunity for math QA systems to test themselves against a benchmark designed to evaluate high school students: The Math SAT (short for Scholastic Achievement Test).

The training and test data consists of unabridged practice exams from various study guides, for the (now retired) exam format administered from 2005 to 2016. We have tagged questions into three broad categories:
- Closed-vocabulary algebra, e.g. "Suppose 3x + y = 15, where x is a positive integer. What is the difference between the largest possible value of y and the smallest possible value of x, assuming that y is also a positive integer?"
- Open-vocabulary algebra, e.g. "At a basketball tournament involving 8 teams, each team played 4 games with each of the other teams. How many games were played at this tournament?"
- Geometry, e.g. "The lengths of two sides of a triangle are (x-2) and (x+2), where x > 2. Which of the following ranges includes all and only the possible values of the third side y?"

A majority of the questions are 5-way multiple choice, and a minority have a numeric answer. Only the Geometry subset contains diagrams.

### Provided Datasets

We provide over 2200 training questions, 500 development questions, and 1000 test questions, all derived from Math SAT study guides. Questions are stored as JSON, using LaTeX to encode mathematical formatting.

```
{
  "id": 846,
  "exam": "source4",
  "sectionNumber": 2,
  "sectionLength": 20,
  "originalQuestionNumber": 18,
  "question": "In the figure above, if the slope of line l is \\(-\\frac{3}{2}\\), what is the area of triangle AOB?",
  "answer": "E",
  "choices": {
    "A": "24",
    "B": "18",
    "C": "16",
    "D": "14",
    "E": "12"
  },
  "diagramRef": "diagram252.png",
  "tags": ["geometry"]
}
```

For more details on the JSON data format, please visit [this page](https://github.com/allenai/semeval2019-task10/blob/master/docs/dataFormat.md).

### Gold Logical Forms

Additionally, we provide gold logical forms for a majority of the training questions in the Closed Algebra track. These logical forms are the same language used in the paper: 

Hopkins, M., Petrescu-Prahova, C., Levin, R., Le Bras, R., Herrasti, A., & Joshi, V. (2017). Beyond sentential semantic parsing: Tackling the math sat with a cascade of tree transducers. In Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing (pp. 795-804). [(pdf)](https://pdfs.semanticscholar.org/c22a/240d1087603664826e9aab809273ed9bff15.pdf?_ga=2.52187753.1130679049.1530133172-566539276.1446829155&_gac=1.6555398.1527028246.EAIaIQobChMI9YuywK-a2wIVlcBkCh0WKw_kEAAYASAAEgKwgPD_BwE)

The logical form language is described [here](https://github.com/allenai/semeval2019-task10/blob/master/docs/logicalFormLanguage.md).
Competitors are free to ignore the provided logical forms if desired. Evaluation will be based solely on a system's ability to answer questions correctly. Competitors will also be free to use additional publicly available math training questions, like AQuA or MAWPS; we ask only that competitors refrain from using additional Math SAT questions found on the web or elsewhere, to avoid potential train/test overlap.

The logical forms are [here](https://github.com/allenai/semeval-2019-task-10/blob/master/interpreter/data/goldLogicalForms_closedAlgebra.json).

We also provide an interpreter for these logical forms. For instructions on how to use the logical form interpreter, see the guide [here](https://github.com/allenai/semeval-2019-task-10/tree/master/interpreter).

### Evaluation

Evaluation will be based solely on a system's ability to answer questions correctly.

For each subtask, the main evaluation metric will simply be question accuracy, i.e. the number of correctly answered questions. The evaluation script takes as input a list of JSON datum { id: \<id\>, response: "\<response\>"}, where \<id\> is the integer index of a question and \<response\> is the guessed response (either a choice key or a numeric string). It will output the system’s score as the number of correct responses divided by the total number of questions in the subtask.

While the main evaluation metric includes no penalties for guessing, we will also compute a secondary metric called penalized accuracy that implements the actual evaluation metric used to score these SATs. This metric is the number of correct questions, minus 1/4 point for each incorrect guess. We include this metric to challenge participants to investigate high-precision QA systems.

### Terms and Conditions

By submitting results to this competition, you consent to the public release of your scores at the SemEval-2018 workshop and in the associated proceedings, at the task organizers' discretion. Scores may include, but are not limited to, automatic and manual quantitative judgments, qualitative judgments, and such other metrics at the task organizers' discretion. You accept that the ultimate decision of metric choice and score value is that of the task organizers. You further agree that the task organizers are under no obligation to release scores and that scores may be withheld if it is the task organizers' judgment that the submission was incomplete, erroneous, deceptive, or violated the letter or spirit of the competition's rules. Inclusion of a submission's scores is not an endorsement of a team or individual's submission, system, or science.

You further agree that your system may be named according to the team name provided at the time of submission, or to a suitable shorthand as determined by the task organizers. You agree to respect the following statements about the dataset:

AI2 makes no warranties regarding the Dataset, including but not limited to being up-to- date, correct or complete. AI2 cannot be held liable for providing access to the Dataset or usage of the Dataset.
The Dataset should only be used for scientific or research purposes related to this competition. Any other use is explicitly prohibited.
You take full responsibility for usage of the Dataset at any time.
AI2 reserves the right to terminate your access to the Dataset at any time.
The Dataset is distributed under "fair use". Copyright will remain with the owners of the content. We will remove data upon request from a copyright owner.
