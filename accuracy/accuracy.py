"""
Predict player accuracy with SciKit.
See README.md
"""

from pandas import DataFrame, read_csv
from sys import path
path.append('..')
from retention import best_feature_classes, plot
from principal import principal_components, explains_text
from score import score_text


answer_count = 5
feature_count = 2
correct_column = 'correct'
item_column = 'item'
response_time_column = 'response_time'
student_column = 'student'
accuracy_column = 'correct_mean'


def aggregate_answers(csv_path, aggregate_path, answer_count = answer_count):
    answers = read_csv(csv_path)
    answers = answers[[student_column, item_column, correct_column, response_time_column]]
    students = answers.groupby(student_column)
    properties = {}
    properties[student_column] = []
    for answer_index in range(answer_count):
        correct = '%s_%s' % (correct_column, answer_index)
        properties[correct] = []
        response_time = '%s_%s' % (response_time_column, answer_index)
        properties[response_time] = []
        item = '%s_%s' % (item_column, answer_index)
        properties[item] = []
    for student_id, student_group in students:
        student_answer_count = len(student_group)
        if student_answer_count < answer_count:
            continue
        properties[student_column].append(student_id)
        corrects = student_group[correct_column].values[:answer_count]
        response_times = student_group[response_time_column].values[:answer_count]
        items = student_group[item_column].values[:answer_count]
        for answer_index in range(answer_count):
            correct = '%s_%s' % (correct_column, answer_index)
            properties[correct].append(corrects[answer_index])
            response_time = '%s_%s' % (response_time_column, answer_index)
            properties[response_time].append(response_times[answer_index])
            item = '%s_%s' % (item_column, answer_index)
            properties[item].append(items[answer_index])
    student_answers = DataFrame(properties)
    append_mean_column(student_answers, answer_count - 1, correct_column)
    append_mean_column(student_answers, answer_count - 1, response_time_column)
    student_answers.to_csv(aggregate_path, index=False)


def plot_accuracy(csv_path, answer_count = answer_count, is_verbose = True,
        classifier_index = -1, is_pca = False, feature_count=feature_count):
    def features_classes(student_answers, feature_count=feature_count, is_verbose=is_verbose):
        class_name = '%s_%s' % (correct_column, answer_count - 1)
        feature_names = [column for column in student_answers.columns]
        feature_names.remove(class_name)
        feature_names.remove(student_column)
        features = student_answers[feature_names].values
        classes = student_answers[[class_name]].values
        if is_pca:
            if is_verbose:
                print(explains_text(features))
            features = principal_components(features, feature_count)
            feature_names = ['component_%s' % index
                for index in range(feature_count)]
        return best_feature_classes(features, classes, feature_names,
            feature_count = feature_count, is_verbose = is_verbose)
    if feature_count <= 2:
        plot(csv_path,
            features_classes = features_classes,
            classifier_index = classifier_index,
            feature_count = feature_count)
    else:
        features, classes = features_classes(read_csv(csv_path))
        return score_text(features, classes, classifier_index)


def summarize(csv_path, answer_count = answer_count, is_verbose = False):
    answers = read_csv(csv_path)
    append_mean_column(answers, answer_count, correct_column)
    if is_verbose:
        print(answers[correct_columns].head())
        print(answers.head())
    accuracy = answers[accuracy_column].mean()
    accuracy = round(accuracy, 2)
    accuracy_text = 'accuracy\n%s' % accuracy
    return accuracy_text


def append_mean_column(answers, answer_count, input_column):
    input_columns = []
    for answer_index in range(answer_count):
        input_columns.append('%s_%s' % (input_column, answer_index))
    answer_count_float = float(answer_count)
    input_sum = answers[input_columns].sum(axis=1)
    answers[input_column + '_mean'] = input_sum / answer_count_float


def accuracy_csv(args):
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', nargs='?', help='Where to read MatMat CSV to aggregate.')
    parser.add_argument('--answer_count', type=int, default=answer_count, help='Number of answers to filter students with.')
    parser.add_argument('--aggregate_path', help='Aggregate students CSV to this file.  Filter students with answer_count or more answers.')
    parser.add_argument('--classifier_index', default=-1, type=int, help='Index of classifier to plot, useful when data is too big to plot multiple classifiers.')
    parser.add_argument('--feature_count', default=feature_count, type=int, help='Maximum number of features or components to classify from.')
    parser.add_argument('--pca', action='store_true', help='Analyze principal components of columns before predicting.')
    parser.add_argument('--plot', action='store_true', help='Plot comparison of classifiers.')
    parser.add_argument('--summarize', action='store_true', help='Print average accuracy per student from aggregated student CSV.')
    parser.add_argument('--test', action='store_true', help='Check examples in README.md.')
    parser.add_argument('--verbose', action='store_true', help='Log steps.')
    parsed = parser.parse_args(args)
    result = None
    if parsed.csv_path:
        if parsed.aggregate_path:
            result = aggregate_answers(parsed.csv_path,
                parsed.aggregate_path,
                answer_count = parsed.answer_count)
        elif parsed.plot:
            result = plot_accuracy(parsed.csv_path,
                answer_count = parsed.answer_count,
                is_verbose = parsed.verbose,
                is_pca = parsed.pca,
                classifier_index = parsed.classifier_index,
                feature_count = parsed.feature_count)
        if parsed.summarize:
            result = summarize(parsed.csv_path,
                answer_count = parsed.answer_count,
                is_verbose = parsed.verbose)
    if parsed.test:
        from doctest import testfile
        testfile('README.md')
    return result


def accuracy_csv_string(args_text):
    args = args_text.split()
    return accuracy_csv(args)


if '__main__' == __name__:
    from sys import argv
    result = accuracy_csv(argv[1:])
    if result:
        print(result)
