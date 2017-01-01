# What behavior predicts replaying in the second week?

> Gameplay measures focus
> on play time (total days, total sessions, total rounds, average
> session duration, average round duration, total elapsed
> play time), intersession measures (current absence time relative
> to the end of the feature window, average time between
> sessions), social interaction (connected friends, player interaction),
> and round-specific statistics (average moves, average
> stars, maximum level).
Page 25, Rapid Prediction of Player Retention in Mobile Free-to-Play Games by A. Drachen
<https://www.aaai.org/ocs/index.php/AIIDE/AIIDE16/paper/download/13995/13590>

> Total Rounds and Total Playtime have the strongest overall
> effect on retention for the single-session feature window.
> Additionally, Average Stars surprisingly has a significant
> negative relationship with retention. We see a positive
> relationship for Average Duration
Page 27.

Also there is a digest version:
<http://www.gamasutra.com/blogs/AndersDrachen/20161102/284620/Rapid_Retention_Prediction_in_Mobile_Games.php>

Features that tended to predict retention were:
* Average time between sessions
* Number of sessions
* Current absence time

"Predicting Player Churn in the Wild"
Fabian Hadiji∗§, Rafet Sifa†
, Anders Drachen‡
, Christian Thurau§
, Kristian Kersting∗†, Christian Bauckhage†¶
§Game Analytics, Berlin, Germany
∗Technical University Dortmund, Dortmund, Germany
†Fraunhofer IAIS, St. Augustin, Germany
‡Aalborg University, Aalborg, Denmark
¶B-IT, University of Bonn, Germany
<http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.651.1731&rep=rep1&type=pdf>

## Dataset

June 2015, Mediatonic provided 3 months of data for analysis.

<https://www.r-bloggers.com/aggregate-player-preference-for-the-first-20-building-created-in-illyriad/>

<https://www.meetup.com/Data-Science-London/events/222708603/>


## Outline

* Will this user play again in their second week?
* Will there be another event from this user in the next 0 to 13 days?

* Tabulate features.
* Group by user.
* Limit last event to 14 days before last event in dataset.
* Derive engagement data.

Tabulate features:

    event
        init
        progress
        ...
    properties.reward
    time

Sort by uid then time.

Group by:

    uid or clientIp

Derive data:

    nth event
    current absence time
    nth day
    number of events in first week
    time since last progress

Classify by decision tree.

Filter CSV to users whose first event was at least 14 days before the last event in dataset.

Randomly sample CSV rows of 4% users with an opportunity to be retained in separate test CSV.

Aggregate user retention CSV.

Split training and test data.  Score the model.

Standardize scale.

<http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html>

Reuse SciKit to split data.

TODO:

Plot example of various models.

For a baseline of noise, predict and compare random data.

<http://scikit-learn.org/stable/modules/model_evaluation.html>

Cross-validate:  Predict retention in test CSV.  Compare to actual retention.

<http://scikit-learn.org/stable/modules/cross_validation.html>

Generalize uid,time,event column names.


## Details

### Tabulating JSON

Memory usage is limited to one 500 MB file at a time.  Example:

    python retention.py data/part-00000.csv ~/Downloads/mediatonic/part-00000

So this file runs all parts:

    bash retention.sh

Mediatonic data sample has rows of JSON, sometimes with trailing whitespace.

Example:


Formatted init:

    {
        "app": "DO",
        "appVersion": "2.4.67.7442",
        "calcDate": "2014-07-25T05:46:27.0000000",
        "clientIp": "66.56.37.0",
        "date": "2014-07-25T05:46:27.342Z",
        "device": "iPod",
        "event": "init",
        "localTime": "1406267184000",
        "platform": "iOS",
        "properties": null,
        "queueDuration": "0",
        "time": 1406267187342,
        "uid": "0001E7ED9ECB34E9A1D31DE15B334E32001B32BD"
    }

Formatted progress:

    {
        "app": "DO",
        "appVersion": "2.4.67.7442",
        "calcDate": "2014-07-25T05:42:23.0000000",
        "clientIp": "66.56.37.0",
        "date": "2014-07-25T05:44:06.836Z",
        "device": "iPod",
        "event": "progress",
        "localTime": "1406266940000",
        "platform": "iOS",
        "properties": {
            "action": "complete",
            "build": {
                "chassis": {
                    "level": 1,
                    "upgradelevel": 1
                },
                "engine": {
                    "level": 1,
                    "upgradelevel": 1
                },
                "gearbox": {
                    "level": 1,
                    "upgradelevel": 1
                },
                "id": "scooter_clone",
                "suspension": {
                    "level": 1,
                    "upgradelevel": 1
                },
                "wheels": {
                    "level": 1,
                    "upgradelevel": 1
                }
            },
            "id": "junkyard_1",
            "package": 100,
            "reward": 1269,
            "type": "race"
        },
        "queueDuration": "103000",
        "time": 1406267046836,
        "uid": "0001E7ED9ECB34E9A1D31DE15B334E32001B32BD"
    }

Init:

    >>> init = '{"time":1406267187342,"date":"2014-07-25T05:46:27.342Z","clientIp":"66.56.37.0","app":"DO","appVersion":"2.4.67.7442","device":"iPod","event":"init","localTime":"1406267184000","platform":"iOS","properties":null,"queueDuration":"0","uid":"0001E7ED9ECB34E9A1D31DE15B334E32001B32BD","calcDate":"2014-07-25T05:46:27.0000000"}	'

Progress:

    >>> progress = '{"time":1406267046836,"date":"2014-07-25T05:44:06.836Z","clientIp":"66.56.37.0","app":"DO","appVersion":"2.4.67.7442","device":"iPod","event":"progress","localTime":"1406266940000","platform":"iOS","properties":{"action":"complete","build":{"chassis":{"level":1,"upgradelevel":1},"engine":{"level":1,"upgradelevel":1},"gearbox":{"level":1,"upgradelevel":1},"id":"scooter_clone","suspension":{"level":1,"upgradelevel":1},"wheels":{"level":1,"upgradelevel":1}},"id":"junkyard_1","package":100,"reward":1269,"type":"race"},"queueDuration":"103000","uid":"0001E7ED9ECB34E9A1D31DE15B334E32001B32BD","calcDate":"2014-07-25T05:42:23.0000000"}	'

Convert to CSV.

    >>> from tabulate import *
    >>> text = init + '\r\n' + progress
    >>> fieldnames = ['uid', 'time', 'event']
    >>> csv_text = jsons_to_csv(text, fieldnames)
    >>> print(csv_text)
    uid,time,event
    0001E7ED9ECB34E9A1D31DE15B334E32001B32BD,1406267046836,progress
    0001E7ED9ECB34E9A1D31DE15B334E32001B32BD,1406267187342,init

### Overview of decision tree

    python retention.py test/user_retention.csv

Simulated command line arguments:

    >>> from retention import *
    >>> print(retention_csv_string('--random_state 0 test/user_retention.csv'))
    Decision tree graphed in file 'test/user_retention.csv.pdf'
    Decision tree score: 0.50

### Derive times

Pandas derived times.  Time stamps make sense as milliseconds.

    >>> progress_2_text = "\n0001E7ED9ECB34E9A1D31DE15B334E32001B32BD,1406367187342,progress"
    >>> user_2_text = "\n2,100,progress\n2,1000000000,progress"
    >>> user_2_csv = csv_text + progress_2_text + user_2_text
    >>> user_2_stream = StringIO(user_2_csv)
    >>> frame = derive_file(user_2_stream)
    >>> frame.head()  #doctest: +NORMALIZE_WHITESPACE
                                            uid           time     event  \
    0  0001E7ED9ECB34E9A1D31DE15B334E32001B32BD  1406267046836  progress
    1  0001E7ED9ECB34E9A1D31DE15B334E32001B32BD  1406267187342      init
    2  0001E7ED9ECB34E9A1D31DE15B334E32001B32BD  1406367187342  progress
    3                                         2            100  progress
    4                                         2     1000000000  progress
    <BLANKLINE>
       nth_event  absence_time  day  no_progress_times  bracket
    0          0           NaN    0                  0        0
    1          1      140506.0    0             140506        0
    2          2   100000000.0    1                  0        0
    3          0           NaN    0                  0        0
    4          1   999999900.0   11                  0        1

MaxU counted the nth row in a group by cumulative count.
<https://stackoverflow.com/questions/17775935/sql-like-window-functions-in-pandas-row-numbering-in-python-pandas-dataframe/36704460#36704460>

EdChum subtracted time since first row in the group.
<http://stackoverflow.com/questions/37634786/using-first-row-in-pandas-groupby-dataframe-to-calculate-cumulative-difference>

I subtracted time since last progress for events that were not progress.  Example:

    >>> sum_no_progress_times([100, 125, 200], ['progress', 'init', 'progress'])
    [0, 25, 0]


### Aggregate bracketed retention

Number of days played in range.  Example:

    >>> retained = aggregate(frame)
    >>> retained
                                            uid  day_0_6  day_7_13
    0                                         2        1         1
    1  0001E7ED9ECB34E9A1D31DE15B334E32001B32BD        2         0


### Aggregate user retention CSV

Format events into user days.

    python retention.py --aggregate_path test/user_retention.csv test/user_4.csv

Example:

    >>> print(retention_csv_string('--aggregate_path test/user_retention.csv test/user_4.csv'))
    test/user_retention.csv
    >>> print(open('test/user_retention.csv.change.csv').read())
    uid,time,event,nth_event,absence_time,day,no_progress_times,bracket
    2,200,progress,0,,0,0,0
    2,604800000,progress,1,604799800.0,6,0,0
    2,604800200,progress,2,200.0,7,0,1
    3,300,progress,0,,0,0,0
    4,400,progress,0,,0,0,0
    <BLANKLINE>
    >>> print(open('test/user_retention.csv').read())
    uid,day_0_6,day_7_13
    2,2,1
    3,1,0
    4,1,0
    <BLANKLINE>


### Decision tree classifies retained

    >>> classifier, score = decision_tree(retained)

To avoid deprecation warning, I reshaped the single feature of days during first bracket.
And I reshaped the sample that is being predicted to be a nested array.

    >>> classifier.predict_proba([[0]])
    array([[ 1.]])

    C:\Python27\lib\site-packages\sklearn\utils\validation.py:395: DeprecationWarning: Passing 1d arrays as data is deprecated in 0.17 and will raise ValueError in 0.19. Reshape your data either using X.reshape(-1, 1) if your data has a single feature or X.reshape(1, -1) if it contains a single sample.
      DeprecationWarning)

<http://stackoverflow.com/questions/37798056/getting-deprecation-warning-in-sklearn-over-1d-array-despite-not-having-a-1d-ar>

### Install GraphViz to write PDF

Windows:
<http://www.graphviz.org/Download_windows.php>

     pip install pydotplus

Include directory of gvedit.exe in system path.
<http://stackoverflow.com/questions/18438997/why-is-pydot-unable-to-find-graphvizs-executables-in-windows-8>

This path is near beginning of paths.
Restart all bash sessions.
<http://superuser.com/questions/607533/windows-git-bash-bash-path-to-read-windows-path-system-variable/939749#939749>

Test GraphViz installation with:

     python decision_tree_example.py

     Probability first iris is in each class of irises: array([[ 1.,  0.,  0.]])
     Decision tree graphed in file 'test/iris.pdf'

### Write PDF

    >>> write_pdf(classifier, 'test/retained.pdf')
    Decision tree graphed in file 'test/retained.pdf'

Because I standardized the features, the features listed are in terms of deviations from the mean.

The 'gini' refers to Gini-impurity, or the probability of misclassifying.
<https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity>
<http://scikit-learn.org/stable/modules/tree.html#classification-criteria>

### Filter users to retention bracket

Suppose the bracket of retention is 7 to 13 days.
If a user started less than 14 days before the end of data collection, the user might not have had the full bracket available.
So I filtered to users whose first event was at least a full bracket before the last event in sample dataset.

For example, in the two users above, user 2's first event is 1970, whereas the first user's event is less than 14 days before the end of that sample, so only user 2 remains.

    >>> user_2_stream = StringIO(user_2_csv)
    >>> print(filter_user_bracket_file(user_2_stream, day_brackets, output_path=None))
    uid,time,event
    2,100,progress
    2,1000000000,progress

Times are in milliseconds.  If your times are not milliseconds, you could modify `time_per_day`.

    >>> time_per_day
    86400000

This can be run from the command line.

    python retention.py --filter_path test/user_3_opportunity.csv test/user_4.csv

Here is an example, simulating command line arguments:

    >>> retention_csv_string('--filter_path test/user_3_opportunity.csv test/user_4.csv')
    'test/user_3_opportunity.csv'
    >>> print(open('test/user_3_opportunity.csv').read())
    uid,time,event
    2,200,progress
    2,604800000,progress
    2,604800200,progress
    3,300,progress
    4,400,progress
    <BLANKLINE>


### Sample training and test CSVs

My function `fit_score` wraps SciKit utility to split training and test data.
<http://scikit-learn.org/stable/modules/cross_validation.html>

I extracted a sample of 4 percent of users to quickly test.

Analyzing a sample of hundreds of thousands of rows took several minutes on my computer.

The smaller sample speeds up testing end-to-end.

SciKit already has another method to test the validity of the data.

Here is a tiny example of 80% users.  The other 20%, rounded to the nearest whole, are saved in a test CSV.

    python retention.py --filter_path test/user_2_opportunity.csv --sample_percent 80 --random_state 2 test/user_4.csv

To test this consistently, I seeded random number generator.

    >>> print(retention_csv_string('--filter_path test/user_2_4_opportunity.csv --sample_percent 80 --random_state 2 test/user_4.csv'))
    test/user_2_4_opportunity.csv
    test/user_2_4_opportunity.csv.test.csv
    >>> print(open('test/user_2_4_opportunity.csv').read())
    uid,time,event
    2,200,progress
    2,604800000,progress
    2,604800200,progress
    4,400,progress
    <BLANKLINE>
    >>> print(open('test/user_2_4_opportunity.csv.test.csv').read())
    uid,time,event
    3,300,progress
    <BLANKLINE>

Different seed may yield different users.

    >>> print(retention_csv_string('--filter_path test/user_3_4_opportunity.csv --sample_percent 80 --random_state 7 test/user_4.csv'))
    test/user_3_4_opportunity.csv
    test/user_3_4_opportunity.csv.test.csv
    >>> print(open('test/user_3_4_opportunity.csv').read())
    uid,time,event
    3,300,progress
    4,400,progress
    <BLANKLINE>
    >>> print(open('test/user_3_4_opportunity.csv.test.csv').read())
    uid,time,event
    2,200,progress
    2,604800000,progress
    2,604800200,progress
    <BLANKLINE>

Pandas extracted unique users.
<http://chrisalbon.com/python/pandas_list_unique_values_in_column.html>
And filtered rows by that sample of users.
<http://stackoverflow.com/questions/12096252/use-a-list-of-values-to-select-rows-from-a-pandas-dataframe>


### Compare various models

If you don't have MatPlot, install:

    pip install matplotlib

Download and run the comparison:

<http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html>

    python plot_classifier_comparison.py

These can be compared with the test dataset.

    bash retention_example.sh

Which calls:

    python retention.py --plot test/part-00000.small.csv.test.user.csv

    >>> print(retention_csv_string('--plot test/part-00000.small.csv.test.user.csv'))


### Reshape 2D

The plot expects 2D.  As a cursory investigation, I only had one dimension:  number of days in first week.

I reshaped the features.

    >>> features1d = array([[20], [21], [22]])
    >>> features2d = set_dimension(features1d, 2)
    >>> features2d
    array([[20,  0],
           [21,  0],
           [22,  0]])
    >>> features2d = set_dimension(features2d, 2)
    >>> features2d
    array([[20,  0],
           [21,  0],
           [22,  0]])

Three dimensional or higher features are truncated:

    >>> features3d = [[20, 30, 40], [21, 31, 41]]
    >>> features2d = set_dimension(features3d, 2)
    >>> features2d
    [[20, 30], [21, 31]]

    >>> features0d = [[], []]
    >>> features2d = set_dimension(features0d, 2)
    >>> features2d
    [[0, 0], [0, 0]]
