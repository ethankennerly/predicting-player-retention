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


## Future directions

Where is the bottleneck in the funnel of answers per user?

What features of the answer predict answering again?

Is this more stable when filtering out players who started in the last week of the sample?

What is second week retention rate?  What is second day in first week retention rate?

How well does 10 question accuracy or any other factors predict second week retention?  Second day in first week retention?
