"""
See README.md
"""


from pandas import DataFrame, read_csv


def sum_no_progress_times(times, events):
    no_progress_times = []
    progress_time = -1
    for time, event in zip(times, events):
        if 'progress' == event or -1 == progress_time:
            progress_time = time
        since = time - progress_time
        no_progress_times.append(since)
    return no_progress_times


def derive_file(csv_path):
    frame = read_csv(csv_path)
    groups = frame.groupby(frame.columns[0])
    frame['nth_event'] = groups.cumcount()
    frame['absence_time'] = groups['time'].diff()
    millisecond_per_day = 1000 * 60 * 60 * 24
    frame['day'] = (frame['time'] - groups['time'].transform('first')) / millisecond_per_day
    frame['day'] = frame['day'].astype(int)
    frame['no_progress_times'] = sum_no_progress_times(frame['time'], frame['event'])
    return frame


def aggregate(frame, day_brackets=[7, 13]):
    template = 'day_%s_%s'
    brackets = [[0, day_brackets[0] - 1], day_brackets]
    uid = frame.groupby('uid')
    properties = {}
    properties['uid'] = uid.groups.keys()
    for start, end in brackets:
        name = template % (start, end)
        # in_range = uid[(uid['day'] >= start) & (uid['day'] <= end)]
        in_range = uid.apply(lambda u: u[(u['day'] >= start) & (u['day'] <= end)])
        properties[name] = in_range['day'].nunique()
    # return properties
    aggregated = DataFrame(properties)
    return aggregated


if '__main__' == __name__:
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', nargs='?', help='Where to read CSV.')
    args = parser.parse_args()
    if args.csv_path:
        derive_file(args.csv_path)
    from doctest import testfile
    testfile('README.md')
