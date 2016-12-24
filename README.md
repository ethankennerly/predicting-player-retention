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

TODO:

Group by:

    uid or clientIp

Limit last event to 14 days before last event in dataset.

Derive data:

    nth day
    nth event
    number of events in first week
    current absence time
    time since last reward
    change in reward since last reward


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

    >>> from retention import *
    >>> text = init + '\r\n' + progress
    >>> fieldnames = ['uid', 'time', 'event']
    >>> csv_text = jsons_to_csv(text, fieldnames)
    >>> print(csv_text)
    uid,time,event
    0001E7ED9ECB34E9A1D31DE15B334E32001B32BD,1406267046836,progress
    0001E7ED9ECB34E9A1D31DE15B334E32001B32BD,1406267187342,init

