"""
See README.md
"""

from collections import defaultdict
from pandas import DataFrame, read_csv
from sklearn.tree import DecisionTreeClassifier


day_brackets = [7, 13]
template = 'day_%s_%s'


def sum_no_progress_times(times, events):
    no_progress_times = []
    progress_time = -1
    for time, event in zip(times, events):
        if 'progress' == event or -1 == progress_time:
            progress_time = time
        since = time - progress_time
        no_progress_times.append(since)
    return no_progress_times


def derive_file(csv_path, day_brackets=day_brackets):
    frame = read_csv(csv_path)
    groups = frame.groupby(frame.columns[0])
    frame['nth_event'] = groups.cumcount()
    frame['absence_time'] = groups['time'].diff()
    millisecond_per_day = 1000 * 60 * 60 * 24
    frame['day'] = (frame['time'] - groups['time'].transform('first')) / millisecond_per_day
    frame['day'] = frame['day'].astype(int)
    frame['no_progress_times'] = sum_no_progress_times(frame['time'], frame['event'])
    frame['bracket'] = frame['day'] / day_brackets[0]
    frame['bracket'] = frame['bracket'].astype(int)
    return frame


def aggregate(frame, day_brackets=day_brackets):
    names = format_names(day_brackets)
    uid_bracket = frame.groupby(['uid', 'bracket'])
    uid = frame.groupby('uid')
    properties = defaultdict(list)
    properties['uid'] = uid.groups.keys()
    bracket_max = frame['bracket'].max()
    for uid in properties['uid']:
        for name in names:
            properties[name].append(0)
    for uid, bracket in uid_bracket.groups:
        uid_index = properties['uid'].index(uid)
        name = names[bracket]
        days = frame[(frame['uid'] == uid) & (frame['bracket'] == bracket)]['day']
        properties[name][uid_index] = days.nunique()
    aggregated = DataFrame(properties)
    return aggregated


def format_names(day_brackets):
    brackets = [[0, day_brackets[0] - 1], day_brackets]
    names = []
    for start, end in brackets:
        name = template % (start, end)
        names.append(name)
    return names


def decision_tree(aggregated, day_brackets=day_brackets):
    classifier = DecisionTreeClassifier()
    names = format_names(day_brackets)
    features = [aggregated[names[0]]]
    classes = aggregated[names[1]]
    print('features %r\nclasses %r' % (features, classes))
    classifier.fit(features, classes)
    return classifier


def decision_tree_retain_1_file(csv_path):
    frame = derive_file(csv_path)
    retained = aggregate(frame)
    classifier = decision_tree(retained)
    return classifer.predict_proba([1])


if '__main__' == __name__:
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', nargs='?', help='Where to read CSV.')
    args = parser.parse_args()
    if args.csv_path:
        decision_tree_retain_1_file(args.csv_path)
    from doctest import testfile
    testfile('README.md')
