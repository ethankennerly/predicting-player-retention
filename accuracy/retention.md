# Predicting retention

What is the per-answer retention rate funnel?

    >>> from retention import *

Using the data sample mentioned in [README.md](README.md).

Summarize funnel in a test sample file:

    >>> funnel_args = '--funnel test/answers_sample.csv'.split()
    >>> print(retention_args(funnel_args))
    test/answers_sample.funnel.csv
    answer_count,cumulative_frequency
    1,46
    2,45
    3,44
    4,43
    5,41
    6,41
    7,41
    8,40
    9,40
    10,40
    11,40
    12,40
    13,40
    14,40
    15,40
    16,40
    17,38
    18,37
    19,37
    20,37
    21,37
    22,37
    23,33
    24,32
    25,29
    26,29
    27,29
    28,29
    29,28
    30,28
    31,28
    32,26
    33,23
    34,23
    35,22
    36,22
    37,20
    38,20
    39,19
    40,10
    41,10
    42,10
    43,9
    44,6
    45,4
    46,4
    <BLANKLINE>

This relies on counting frequencies less than or equal to a value.

    >>> reverse_cumulative_range([1, 4, 2, 2])
    array([4, 3, 1, 1])

## Future directions

Where is the bottleneck in the funnel of answers per user?

What features of the answer predict answering again?

Is this more stable when filtering out players who started in the last week of the sample?

What is second week retention rate?  What is second day in first week retention rate?

How well does 10 question accuracy or any other factors predict second week retention?  Second day in first week retention?
