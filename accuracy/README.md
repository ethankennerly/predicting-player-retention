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

Aggregate students into their first five answers.

For each student answer:
    item
    response_time
    correct

Split students into training and test datasets.

All columns except 5th answer correct are potential features.

5th answer correct is the target.

Select two best features.

Score the model.


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
