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

### Results

Decision tree, neural net, and some others predicted with a score of 0.84 by the value by the correctness of answers 4 and 5.  Random prediction would score 0.50.  So there is about a 1 in 6 chance of being wrong in this sample.

Example decision tree:

![](student_answers.csv.classifier_Decision_Tree.png)


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
    1,1,54,56,15060,9735,33183
    1,1,2,22,45203,63256,33184
    0,0,38,51,57276,17068,33480
    0,1,685,148,19878,12359,33481
    0,1,1737,1787,3911,10101,33482
    1,1,1434,1501,12542,7564,33483
    1,1,1737,1822,9419,4030,33485
    1,1,47,50,9800,5667,33486
    1,1,1737,1822,6066,3114,33489
    1,1,47,50,25734,6398,33490
    1,1,1448,1485,10910,7234,33491
    0,0,1434,1562,10971,14415,33492
    1,1,1409,1672,12076,7734,33495
    1,1,1434,1501,6508,7346,33496
    1,1,1674,1367,46085,30704,33497
    0,1,47,50,4618,4364,33498
    1,1,1723,1434,11147,5973,33499
    0,0,356,667,15785,39712,33500
    1,1,1562,1554,16716,19971,33501
    1,0,1737,1822,8686,8443,33502
    1,1,1562,1309,13582,11400,33504
    1,1,1723,1822,13271,5125,33505
    1,1,1696,1423,6356,6342,33506
    0,1,50,47,16681,19024,33507
    0,0,356,447,21742,26750,33508
    1,1,1723,1696,6057,5284,33509
    1,1,1278,1367,37351,6602,33510
    1,1,1043,1698,51156,29908,33512
    1,1,512,361,4405,4367,33522
    1,0,356,243,13272,6337,33532
    1,1,516,416,18608,8886,33533
    1,0,50,41,8663,2920,33537
    1,1,1562,1822,15852,144131,33538
    1,0,1045,1562,19888,4374,33540
    1,1,50,47,43807,23277,33541
    1,0,1434,1501,19657,11984,33542
    1,1,1737,1822,6639,3646,33543
    1,0,1045,1689,22849,12862,33544
    1,0,1111,1492,6607,12794,33545
    0,1,50,47,5361,16895,33546
    0,1,880,1723,13279,14234,33547
    1,1,1562,1434,21309,21573,33548
    1,0,1434,1505,35337,4099,33549
    1,1,1309,1587,25735,12501,33550
    1,1,923,1528,14128,36749,33551
    <BLANKLINE>

#### Plotting accuracy prediction

    bash accuracy.sh

Quick example of usage:

    >>> accuracy_csv_string('--plot test/student_answers_sample.csv --answer_count 2') #doctest: +ELLIPSIS
    features_classes: features: ['correct_0', 'item_0', 'item_1', 'response_time_0', 'response_time_1']
    ...
    plot_comparison: Saved figure to: 'test/student_answers_sample.csv.png'

![](test/student_answers_sample.csv.png)



## Future directions

Aggregate accuracy of 5 answers is 82%.  The decision tree predicts 84% of the time.  The difference between the predictor and mean accuracy is negligible.

    >>> print(accuracy_csv_string('--summarize test/student_answers_sample.csv --answer_count 2'))
    accuracy
    0.76

Would 9 answers increase accuracy of predicting 10th answer?

Would principal component analysis increase predicted accuracy?
<https://www.analyticsvidhya.com/blog/2016/03/practical-guide-principal-component-analysis-python/>
<https://plot.ly/ipython-notebooks/principal-component-analysis/>
<http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html>

What is second week retention rate?  What is second day in first week retention rate?

How well does 10 question accuracy or any other factors predict second week retention?  Second day in first week retention?


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
