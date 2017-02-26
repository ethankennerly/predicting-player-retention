"""
See README.md
"""

from StringIO import StringIO
from collections import defaultdict
from itertools import compress
from math import isnan
from numpy import append, array, copy, delete
from pandas import DataFrame, read_csv
from pydotplus import graph_from_dot_data
from random import random, randrange, seed, shuffle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_classif


day_brackets = [7, 13]
template = 'day_%s_%s'
time_per_day = 1000 * 60 * 60 * 24
time_names = [
    'absence_time',
    'no_progress_times',
]
uid_column = 'uid'
time_column = 'time'
event_column = 'event'


def to_csv(frame):
    stream = StringIO()
    frame.to_csv(stream, index=False)
    return stream.getvalue().strip()


def extract_features(frame, class_name, ignore_columns = []):
    feature_names = [column for column in frame.columns]
    feature_names.remove(class_name)
    for column in ignore_columns:
        if column in feature_names:
            feature_names.remove(column)
    features = frame[feature_names].values
    classes = frame[[class_name]].values
    return features, classes, feature_names


def sample_users(user_time, percent, random_state=None):
    uniques = user_time[uid_column].unique()
    if random_state is not None:
        seed(random_state)
    shuffle(uniques)
    fraction = percent / 100.0
    user_count = int(round(len(uniques) * fraction))
    a_sample_users = uniques[:user_count]
    b_sample_users = uniques[user_count:]
    a_sample = user_time[user_time[uid_column].isin(a_sample_users)]
    b_sample = user_time[user_time[uid_column].isin(b_sample_users)]
    samples = [a_sample, b_sample]
    return samples


def filter_user_bracket_file(csv_path, day_brackets=day_brackets,
        output_path=None, sample_percent=-1, random_state=None):
    day = day_brackets[-1] + 1
    time = day * time_per_day
    user_time = read_csv(csv_path)
    time_max = user_time[time_column].max()
    time_limit = time_max - time
    users = user_time.groupby(uid_column)
    user_time['first'] = users[time_column].transform('first')
    user_time = user_time[user_time['first'] <= time_limit]
    del user_time['first']
    samples = [user_time]
    output_paths = [output_path]
    results = []
    if 0 <= sample_percent:
        samples = sample_users(user_time, sample_percent, random_state)
        output_paths.append(output_path + '.test.csv')
    for sample, output_path in zip(samples, output_paths):
        if output_path:
            sample.to_csv(output_path, index=False)
            results.append(output_path)
        else:
            results.append(to_csv(user_time))
    return '\n'.join(results)


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
    frame['absence_time'] = groups[time_column].diff()
    frame['day'] = (frame[time_column] - groups[time_column].transform('first')) / time_per_day
    frame['day'] = frame['day'].astype(int)
    frame['no_progress_times'] = sum_no_progress_times(frame[time_column], frame[event_column])
    frame['bracket'] = frame['day'] / day_brackets[0]
    frame['bracket'] = frame['bracket'].astype(int)
    return frame


def aggregate(frame, day_brackets=day_brackets):
    names = format_names(day_brackets)
    uid_bracket = frame.groupby([uid_column, 'bracket'])
    uid = frame.groupby(uid_column)
    properties = defaultdict(list)
    properties[uid_column] = uid.groups.keys()
    bracket_max = frame['bracket'].max()
    time_bracket = day_brackets[0] * time_per_day
    for uid in properties[uid_column]:
        for name in names:
            properties[name].append(0)
        for time in time_names:
            properties[time].append(0)
            properties[time + '_current'].append(0)
    names_length = len(names)
    for uid, bracket in uid_bracket.groups:
        uid_index = properties[uid_column].index(uid)
        if bracket < names_length:
            try:
                name = names[bracket]
                in_bracket = frame[(frame[uid_column] == uid) & (frame['bracket'] == bracket)]
                days = in_bracket['day']
                properties[name][uid_index] = days.nunique()
            except:
                print('aggregate: bracket %r not in names %r' % (bracket, names))
            if 0 == bracket:
                for time in time_names:
                    value = in_bracket[time].mean()
                    if isnan(value):
                        value = -1
                    properties[time][uid_index] = value
                    time_min = in_bracket[time].min()
                    time_max = in_bracket[time].max()
                    if isnan(time_min):
                        time_min = -1
                    if isnan(time_max):
                        time_max = -1
                    properties[time + '_current'][uid_index] = time_bracket - (time_max - time_min)
    columns = [uid_column]
    columns.extend(names)
    for time in time_names:
        columns.append(time)
        columns.append(time + '_current')
    aggregated = DataFrame(properties, columns=columns)
    return aggregated


def aggregate_file(csv_path, output_path):
    event_text = filter_user_bracket_file(csv_path)
    event_stream = StringIO(event_text)
    change_frame = derive_file(event_stream)
    change_frame.to_csv(output_path + '.change.csv', index=False)
    retained = aggregate(change_frame)
    retained.to_csv(output_path, index=False)
    return output_path


def format_names(day_brackets):
    brackets = [[0, day_brackets[0] - 1], day_brackets]
    names = []
    for start, end in brackets:
        name = template % (start, end)
        names.append(name)
    return names


def fit_score(classifier, features, classes, random_state=None):
    X_train, X_test, y_train, y_test = train_test_split(
        features, classes, test_size=0.4, random_state=random_state)
    scaler = StandardScaler().fit(X_train.astype(float))
    X_train_transformed = scaler.transform(X_train.astype(float))
    X_test_transformed = scaler.transform(X_test.astype(float))
    classifier = classifier.fit(X_train_transformed, y_train)
    score = classifier.score(X_test_transformed, y_test)
    return classifier, score


def features_classes(aggregated, day_brackets=day_brackets, feature_count=2, is_binary=True, is_verbose=False):
    feature_name, class_name = format_names(day_brackets)
    feature_names = [feature_name]
    for time in time_names:
        feature_names.append(time)
        feature_names.append(time + '_current')
    features = aggregated[feature_names].values
    classes = aggregated[class_name].values
    if is_binary:
        def binary(x):
            if 1 <= x:
                return 1
            else:
                return 0
        classes = array([binary(cls) for cls in classes])
    return best_feature_classes(features, classes, feature_names,
        feature_count = feature_count, is_verbose = is_verbose)


def best_feature_classes(features, classes, feature_names, feature_count = 2, is_verbose = False):
    threshold = VarianceThreshold()
    features_vary = threshold.fit_transform(features)
    feature_names = [name for name in compress(feature_names, threshold.get_support())]
    best = SelectKBest(f_classif, k=feature_count)
    best_features = best.fit_transform(features_vary, classes)
    if is_verbose:
        print('features_classes: features: %r\n    feature sample %r\n    scores %r\n    p-values %r\n    support %r' % (
            feature_names, features_vary[0], best.scores_, best.pvalues_, best.get_support()))
    return best_features, classes


def decision_tree(aggregated, day_brackets=day_brackets):
    names = format_names(day_brackets)
    features, classes = features_classes(aggregated, day_brackets)
    classifier = DecisionTreeClassifier()
    return fit_score(classifier, features, classes)


def write_pdf(classifier, pdf_path):
    dot_data = export_graphviz(classifier, out_file=None)
    graph = graph_from_dot_data(dot_data)
    graph.write_pdf(pdf_path)
    print('Decision tree graphed in file %r' % pdf_path)


def decision_tree_retain_1_file(csv_path):
    retained = read_csv(csv_path)
    classifier, score = decision_tree(retained)
    write_pdf(classifier, csv_path + '.pdf')
    return 'Decision tree score: %0.2f' % score


def set_dimension(table, min_row_length, max_row_length = None):
    is_array = hasattr(table, 'tolist')
    if is_array:
        shaped = table.tolist()
    else:
        shaped = table[:]
    for row in shaped:
        while len(row) < min_row_length:
            if len(row) == 0:
                value = 0
            else:
                value = row[-1]
            row.append(value)
        if max_row_length:
            while max_row_length < len(row):
                del row[-1]
    if is_array:
        shaped = array(shaped)
    return shaped


def plot(csv_path, is_verbose=True, random_state=None, classifier_index=-1,
        features_classes = features_classes, feature_count = 2):
    from plot_classifier_comparison import plot_comparison, all_classifiers, sample_classifiers
    retained = read_csv(csv_path)
    if classifier_index <= -1:
        feature_counts = [feature_count, 1]
    else:
        feature_counts = [feature_count]
    datasets = []
    for feature_count in feature_counts:
        features, classes = features_classes(retained, feature_count=feature_count, is_verbose=is_verbose)
        datasets.append((features, classes))
    if classifier_index <= -1:
        for feature_count in feature_counts:
            datasets.append(random_features_classes(feature_count, random_state=random_state))
    names, classifiers = all_classifiers()
    infix = ''
    if 0 <= classifier_index:
        names = [names[classifier_index]]
        classifiers = [classifiers[classifier_index]]
        infix = '.classifier_%s' % names[0].replace(' ', '_')
    plot_comparison(datasets, names, classifiers, is_verbose=is_verbose,
        output_path=csv_path + infix + '.png')


def random_features_classes(feature_count=2, sample_count=256, class_count=2, random_state=None):
    if random_state:
        seed(random_state)
    features = []
    classes = []
    for sample in range(sample_count):
        feature_row = []
        for feature in range(feature_count):
            feature_row.append(random())
        features.append(feature_row)
        classes.append(randrange(class_count))
    return features, classes


def retention_csv(args):
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', nargs='?', help='Where to read CSV.')
    parser.add_argument('--filter_path', help='Just filter CSV to this file.')
    parser.add_argument('--aggregate_path', help='Aggregate users CSV to this file.  Filter users who have a full bracket to potentially be retained.')
    parser.add_argument('--plot', action='store_true', help='Plot various classifiers.')
    parser.add_argument('--classifier_index', default=-1, type=int, help='Index of classifier to plot, useful when data is too big to plot multiple classifiers.')
    parser.add_argument('--sample_percent', default=-1, type=int, help='During filter, randomly sample up to this percent of users.  Example 80 represents 80%.  The other 20% are placed in a ".test.csv"')
    parser.add_argument('--random_state', default=None, help='Consistently reproduce the same random sample with this seed string.')
    parser.add_argument('--test', action='store_true', help='Check examples in README.md.')
    parsed = parser.parse_args(args)
    result = None
    if parsed.csv_path:
        if parsed.aggregate_path:
            result = aggregate_file(parsed.csv_path, parsed.aggregate_path)
        elif parsed.filter_path:
            result = filter_user_bracket_file(parsed.csv_path, output_path=parsed.filter_path,
                sample_percent=parsed.sample_percent, random_state=parsed.random_state)
        else:
            result = decision_tree_retain_1_file(parsed.csv_path)
        if parsed.plot:
            plot(parsed.csv_path, random_state=parsed.random_state, classifier_index=parsed.classifier_index)
    if parsed.test:
        from doctest import testfile
        testfile('README.md')
    return result


def retention_csv_string(args_text):
    args = args_text.split()
    return retention_csv(args)


if '__main__' == __name__:
    from sys import argv
    result = retention_csv(argv[1:])
    if result:
        print(result)
