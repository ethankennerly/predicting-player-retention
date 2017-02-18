"""
See retention.md
"""


from argparse import ArgumentParser
from doctest import testfile
from numpy import histogram, hstack
from os.path import splitext
from pandas import DataFrame, read_csv
# from scipy.stats import cumfreq
from sys import argv


def reverse_cumulative_range(items):
    counts, binedge = histogram(items, bins=len(items))
    reverse = counts[::-1]
    cumulative = reverse.cumsum()
    return cumulative[::-1]


def funnel(answer_csv):
    answers = read_csv(answer_csv)
    students = answers.groupby('student')
    answer_counts = []
    funnel_properties = {}
    for student_id, student_group in students:
        answer_count = -len(student_group)
        answer_counts.append(answer_count)
    funnel_properties['answer_count'] = range(1, len(answer_counts) + 1)
    funnel_properties['cumulative_frequency'] = reverse_cumulative_range(answer_counts)
    funnel = DataFrame(funnel_properties)
    funnel_csv = '%s.funnel.csv' % splitext(answer_csv)[0]
    funnel.to_csv(funnel_csv, index=False)
    return '%s\n%s' % (funnel_csv, open(funnel_csv).read())


def retention_args(args):
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--funnel_csv', action='store_true', help='From CSV count number of students who answered at least this many times.')
    parser.add_argument('--test', action='store_true', help='Compare examples in retention.md')
    parser.add_argument('answer_csv', nargs='?', help='CSV of student answers.')
    parsed = parser.parse_args(args)
    result = None
    if parsed.funnel_csv:
        result = funnel(parsed.answer_csv)
    if parsed.test:
        testfile('retention.md')
    return result


if '__main__' == __name__:
    result = retention_args(argv[1:])
    if result:
        print(result)
