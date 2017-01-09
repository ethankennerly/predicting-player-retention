"""
Predict player accuracy with SciKit.
See README.md
"""

from pandas import DataFrame, read_csv


answer_count = 5
correct_column = 'correct'
item_column = 'item'
response_time_column = 'response_time'
student_column = 'student'


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
    student_answers.to_csv(aggregate_path, index=False)


def accuracy_csv(args):
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', nargs='?', help='Where to read MatMat CSV to aggregate.')
    parser.add_argument('--answer_count', type=int, default=answer_count, help='Number of answers to filter students with.')
    parser.add_argument('--aggregate_path', help='Aggregate students CSV to this file.  Filter students with answer_count or more answers.')
    parser.add_argument('--test', action='store_true', help='Check examples in README.md.')
    parsed = parser.parse_args(args)
    result = None
    if parsed.csv_path:
        if parsed.aggregate_path:
            result = aggregate_answers(parsed.csv_path, parsed.aggregate_path, answer_count = parsed.answer_count)
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
