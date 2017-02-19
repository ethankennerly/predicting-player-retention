# Predicting retention


## Funnel

What is the per-answer retention rate funnel?

    >>> from retention import *

Using the data sample mentioned in [README.md](README.md).

Summarize funnel in a test sample file:

    >>> funnel_args = '--funnel test/answers_sample_small.csv'.split()
    >>> print(retention_args(funnel_args))
    test/answers_sample_small.funnel.csv
    answer_count,retention_count,step_retention,total_retention
    1,2,1.000,1.000
    2,2,1.000,1.000
    3,1,0.500,0.500
    <BLANKLINE>

The retention count depends on counting frequencies less than or equal to a value.

    >>> reverse_cumulative_frequency([1, 4, 2, 2, 8])
    array([5, 4, 2, 2, 1, 1, 1, 1])

    >>> reverse_cumulative_frequency([2, 3])
    array([2, 2, 1])

Total retention rate depends on retention rate.

    >>> retention_counts = [5, 4, 2, 2, 1, 1, 1, 1]
    >>> retention_rates(retention_counts)
    [1.0, 0.8, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2]
    >>> retention_steps(retention_counts)
    [1.0, 0.8, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0]

## Bottleneck

Where is the bottleneck in the funnel of answers per user?

The funnel step retention shows a drop off after the first and each tenth answer.

Example from:

    python retention.py --funnel data/answers.csv

    answer_count,retention_count,step_retention,total_retention
    1,18847,1.000,1.000
    2,16558,0.879,0.879
    3,15132,0.914,0.803
    4,14151,0.935,0.751
    5,13388,0.946,0.710
    6,12791,0.955,0.679
    7,12317,0.963,0.654
    8,11968,0.972,0.635
    9,11668,0.975,0.619
    10,11353,0.973,0.602
    11,8408,0.741,0.446
    12,7971,0.948,0.423
    13,7637,0.958,0.405

The authors wrote the tenth question is an unadapted difficulty to assess learning.

Or perhaps there is a session break every ten questions.


## Predicting step retention

What features of the answer predict answering the next question?

Mark each student's last question by having no future question.

    >>> feature_args = '--feature test/answers_sample_small.csv'.split()
    >>> print(retention_args(feature_args))
    test/answers_sample_small.feature.csv
    id,time,item,student,response_time,correct,answer,answer_expected,log,random,future_questions,is_future_question
    273951,2016-04-17 14:12:09,38,33480,57276,0,14,13,"{""client_meta"": [[38008, ""13 selected""], [39224, ""unselected""], [49135, ""1 selected""], [55376, ""14 selected""], [57276, ""finished""]], ""device"": ""desktop""}",0,2,True
    273952,2016-04-17 14:12:32,51,33480,17068,0,3,17,"{""client_meta"": [[11382, ""soft-keyboard:3""], [11382, ""3""], [17068, ""finished""]], ""device"": ""desktop""}",0,1,True
    273953,2016-04-17 14:12:45,685,33481,19878,0,95,85,"{""client_meta"": [[13513, ""9""], [18550, ""95""], [19878, ""finished""]], ""device"": ""desktop""}",0,1,True
    273954,2016-04-17 14:13:03,427,33480,15139,1,20,20,"{""client_meta"": [[12145, ""2""], [12399, ""20""], [15139, ""finished""]], ""device"": ""desktop""}",0,0,False
    273955,2016-04-17 14:13:04,148,33481,12359,1,10,10,"{""client_meta"": [[10680, ""1""], [11409, ""10""], [12359, ""finished""]], ""device"": ""desktop""}",0,0,False
    <BLANKLINE>

## Future directions

Is this more stable when filtering out players who started in the last week of the sample?

What is second week retention rate?  What is second day in first week retention rate?

How well does 10 question accuracy or any other factors predict second week retention?  Second day in first week retention?
