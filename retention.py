"""
See README.md
"""


from pandas import read_csv


def derive_file(csv_path):
    frame = read_csv(csv_path)
    groups = frame.groupby(frame.columns[0])
    frame['nth_event'] = groups.cumcount()
    frame['absence_time'] = groups['time'].diff()
    second_per_day = 60 * 60 * 24
    frame['day'] = (frame['time'] - groups['time'].transform('first')) / second_per_day
    frame['day'] = frame['day'].astype(int)
    return frame


if '__main__' == __name__:
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', nargs='?', help='Where to read CSV.')
    args = parser.parse_args()
    if args.csv_path:
        derive_file(args.csv_path)
    from doctest import testfile
    testfile('README.md')
