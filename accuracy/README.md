# Predicting player accuracy

## Prerequisite

[Predicting player retention](../README.md)

## Classifying correctness

How well would would SciKit Learn classify correctness of problem number 5?

### Dataset

Adaptive Learning published datasets of MatMat:
<http://www.fi.muni.cz/adaptivelearning/?a=data>

Described here:
<https://github.com/adaptive-learning/matmat-web/blob/master/data/data_description.md>

Downloaded here:
<http://www.fi.muni.cz/adaptivelearning/data/matmat/>

Adaptive Learning modeled arithmetic skill.
<http://www.fi.muni.cz/adaptivelearning/documents/matmat-model.pdf>

Adaptive Learning published a prediction algorithm.
<https://github.com/adaptive-learning/matmat-web/blob/master/matmat/prediction.py>

### Outline

TODO:

Aggregate students into their first five answers for students with five answers or more.

For each student answer:
    item
    response_time
    correct

Split students into training and test datasets.

All columns except 5th answer correct are potential features.

5th answer correct is the target.

Select two best features.

Score the model.

### Details

#### Aggregating students

Install MatMat dataset into directory:

    data

There is an answers CSV there:

    >>> from os.path import exists
    >>> exists('data/answers.csv')
    True

To aggregate first few student answers:

    python accuracy.py --aggregate_path data/student_answers.csv data/answers.csv

That can take a while.  To quickly test, aggregated students by correct, response time, and item in first 2 answers.

    >>> from accuracy import *
    >>> accuracy_csv_string('--aggregate_path test/student_answers_sample.csv test/answers_sample.csv --answer_count 2')
    >>> print(open('test/student_answers_sample.csv').read())
    correct_0,correct_1,item_0,item_1,response_time_0,response_time_1,student
    0,0,38,51,57276,17068,33480
    0,1,685,148,19878,12359,33481
    0,1,1737,1787,3911,10101,33482
    <BLANKLINE>


# Related work

Adaptive Learning published datasets of geography, arithmetic, and anatomy.
<http://www.fi.muni.cz/adaptivelearning/?a=data>

The arithmetic data set has an intuitive measurement of problem difficulty.

Adaptive Learning experimented with the target accuracy to conclude easier questions engage immediately and harder questions engage after 10 hours.
<http://www.fi.muni.cz/~xpelanek/publications/its-target-difficulty.pdf>

They made the data available.
<http://www.fi.muni.cz/adaptivelearning/data/slepemapy/2016-ab-target-difficulty.zip>

Adaptive Learning has studied adaptive practice, student modeling and problem solving times.
<http://www.fi.muni.cz/adaptivelearning/?a=publications>

Adaptive Learning modeled problem solving times with an iterative estimation of problem difficulty, discrimination, chance solution, and student ability.
<http://www.fi.muni.cz/~xpelanek/publications/sofsem12.pdf>
