"""
Predict player accuracy with SciKit.
See README.md
"""

from pandas import DataFrame, read_csv


student_column = 'student'


def aggregate_answers(csv_path, aggregate_path):
    answers = read_csv(csv_path)
    students = answers.groupby(student_column)
    properties = {}
    student_answers = DataFrame(properties)
    student_answers.to_csv(aggregate_path, index=False)


def accuracy_csv(args):
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', nargs='?', help='Where to read MatMat CSV to aggregate.')
    parser.add_argument('--aggregate_path', help='Aggregate students CSV to this file.  Filter students with five or more answers.')
    parser.add_argument('--test', action='store_true', help='Check examples in README.md.')
    parsed = parser.parse_args(args)
    result = None
    if parsed.csv_path:
        if parsed.aggregate_path:
            result = aggregate_answers(parsed.csv_path, parsed.aggregate_path)
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
