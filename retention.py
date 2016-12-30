"""
See README.md
"""

from collections import defaultdict
from StringIO import StringIO
from pandas import DataFrame, read_csv
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from pydotplus import graph_from_dot_data


day_brackets = [7, 13]
template = 'day_%s_%s'
time_per_day = 1000 * 60 * 60 * 24


def to_csv(frame):
    stream = StringIO()
    frame.to_csv(stream, index=False)
    return stream.getvalue().strip()


def filter_user_bracket_file(csv_path, day_brackets=day_brackets, output_path=None):
    day = day_brackets[-1] + 1
    time = day * time_per_day
    user_time = read_csv(csv_path)
    time_max = user_time['time'].max()
    time_limit = time_max - time
    users = user_time.groupby('uid')
    user_time['first'] = users['time'].transform('first')
    user_time = user_time[user_time['first'] <= time_limit]
    del user_time['first']
    if output_path:
        user_time.to_csv(output_path, index=False)
        return output_path
    else:
        return to_csv(user_time)


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
    frame['day'] = (frame['time'] - groups['time'].transform('first')) / time_per_day
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
    names_length = len(names)
    for uid, bracket in uid_bracket.groups:
        uid_index = properties['uid'].index(uid)
        if bracket < names_length:
            try:
                name = names[bracket]
                days = frame[(frame['uid'] == uid) & (frame['bracket'] == bracket)]['day']
                properties[name][uid_index] = days.nunique()
            except:
                print('aggregate: bracket %r not in names %r' % (bracket, names))
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
    features = aggregated[names[0]].values
    features = [[feature] for feature in features]
    classes = aggregated[names[1]].values
    ## print('features\n%r\nclasses\n%r' % (features, classes))
    classifier.fit(features, classes)
    return classifier


def write_pdf(classifier, pdf_path):
    dot_data = export_graphviz(classifier, out_file=None)
    graph = graph_from_dot_data(dot_data)
    graph.write_pdf(pdf_path)
    print('Decision tree graphed in file %r' % pdf_path)


def decision_tree_retain_1_file(csv_path):
    frame = derive_file(csv_path)
    retained = aggregate(frame)
    classifier = decision_tree(retained)
    write_pdf(classifier, csv_path + '.pdf')
    return classifier.predict_proba([1])


def retention_csv(args):
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', nargs='?', help='Where to read CSV.')
    parser.add_argument('--filter_path', help='Just filter CSV to this file.')
    parsed = parser.parse_args(args)
    if parsed.csv_path:
        if parsed.filter_path:
            return filter_user_bracket_file(parsed.csv_path, output_path=parsed.filter_path)
        else:
            return decision_tree_retain_1_file(parsed.csv_path)


def retention_csv_string(args_text):
    args = args_text.split()
    return retention_csv(args)


if '__main__' == __name__:
    from sys import argv
    retention_csv(argv[1:])
    from doctest import testfile
    testfile('README.md')
