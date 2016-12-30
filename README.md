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

Randomly sample CSV rows of 10 users with an opportunity to be retained.  

TODO:

Randomly assign 80% users to training CSV and 20% to test CSV.

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


### Derive times

Pandas derived times.  Time stamps make sense as milliseconds.

    >>> progress_2_text = "\n0001E7ED9ECB34E9A1D31DE15B334E32001B32BD,1406367187342,progress"
    >>> user_2_text = "\n2,100,progress\n2,1000000000,progress"
    >>> user_2_csv = csv_text + progress_2_text + user_2_text
    >>> user_2_stream = StringIO(user_2_csv)
    >>> from retention import *
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
       day_0_6  day_7_13                                       uid
    0        1         1                                         2
    1        2         0  0001E7ED9ECB34E9A1D31DE15B334E32001B32BD


### Decision tree classifies retained

    >>> classifier = decision_tree(retained)
    >>> classifier.predict_proba([0])
    array([[ 0.,  1.]])


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
    2,2000000000,progress
    3,300,progress
    4,400,progress
    <BLANKLINE>


### Randomly sample JSON

Analyzing a sample of hundreds of thousands of rows took several minutes on my computer.

To quickly test end-to-end, I extracted a sample of 10 users.

    python retention.py --filter_path test/user_2_opportunity.csv --user_sample 2 --random_seed 2 test/user_4.csv

To test this consistently, I seeded random number generator.

    >>> retention_csv_string('--filter_path test/user_2_4_opportunity.csv --user_sample 2 --random_seed 2 test/user_4.csv')
    'test/user_2_4_opportunity.csv'
    >>> print(open('test/user_2_4_opportunity.csv').read())
    uid,time,event
    2,200,progress
    2,2000000000,progress
    4,400,progress
    <BLANKLINE>

Different seed may yield different users.

    >>> retention_csv_string('--filter_path test/user_3_4_opportunity.csv --user_sample 2 --random_seed 7 test/user_4.csv')
    'test/user_3_4_opportunity.csv'
    >>> print(open('test/user_3_4_opportunity.csv').read())
    uid,time,event
    3,300,progress
    4,400,progress
    <BLANKLINE>

Pandas got unique users.
<http://chrisalbon.com/python/pandas_list_unique_values_in_column.html>
And filtered rows by that sample of users.
<http://stackoverflow.com/questions/12096252/use-a-list-of-values-to-select-rows-from-a-pandas-dataframe>
