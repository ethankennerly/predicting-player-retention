"""
See retention.md
"""


from argparse import ArgumentParser
from doctest import testfile
from numpy import cumsum, histogram
from os.path import splitext
from pandas import DataFrame, read_csv
from sys import argv


def reverse(items):
    return items[::-1]


def reverse_cumulative_frequency(items):
    bins = range(1, max(items) + 2)
    counts, binedge = histogram(items, bins=bins)
    return reverse(reverse(counts).cumsum())


def retention_rates(retention_counts):
    rates = []
    total = float(retention_counts[0])
    for count in retention_counts:
        rate = count / total
        rates.append(rate)
    return rates


def retention_steps(retention_counts):
    rates = []
    previous = float(retention_counts[0])
    for count in retention_counts:
        rate = count / previous
        rates.append(rate)
        previous = float(count)
    return rates


def is_future_question(answers):
    future_questions = answers.groupby('student').cumcount(ascending=False)
    answers['future_questions'] = future_questions
    answers['is_future_question'] = True
    answers.loc[answers['future_questions'] <= 0, 'is_future_question'] = False


def feature(answer_csv):
    answers = read_csv(answer_csv)
    is_future_question(answers)
    return save_csv(answers, answer_csv, 'feature')


def save_csv(answers, answer_csv, infix):
    feature_csv = '%s.%s.csv' % (splitext(answer_csv)[0], infix)
    answers.to_csv(feature_csv, index=False, float_format='%.3f')
    return '%s\n%s' % (feature_csv, ''.join(open(feature_csv).readlines()[:10]))


def funnel(answer_csv):
    answers = read_csv(answer_csv)
    students = answers.groupby('student')
    answer_counts = []
    funnel_properties = {}
    for student_id, student_group in students:
        answer_count = len(student_group)
        answer_counts.append(answer_count)
    funnel_properties['answer_count'] = range(1, max(answer_counts) + 1)
    funnel_properties['retention_count'] = reverse_cumulative_frequency(answer_counts)
    funnel_properties['total_retention'] = retention_rates(funnel_properties['retention_count'])
    funnel_properties['step_retention'] = retention_steps(funnel_properties['retention_count'])
    funnel = DataFrame(funnel_properties)
    return save_csv(funnel, answer_csv, 'funnel')


def retention_args(args):
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--feature', action='store_true',
        help='Extend table with is next question answered, time, response time and correctness difference.')
    parser.add_argument('--funnel_csv', action='store_true',
        help='From CSV count number of students who answered at least this many times.')
    parser.add_argument('--test', action='store_true',
        help='Compare examples in retention.md')
    parser.add_argument('answer_csv', nargs='?',
        help='CSV of student answers.')
    parsed = parser.parse_args(args)
    result = None
    if parsed.funnel_csv:
        result = funnel(parsed.answer_csv)
    if parsed.feature:
        result = feature(parsed.answer_csv)
    if parsed.test:
        testfile('retention.md')
    return result


if '__main__' == __name__:
    result = retention_args(argv[1:])
    if result:
        print(result)
