"""
See README.md
"""


from json import loads
from StringIO import StringIO
from csv import writer


fieldnames=['uid', 'time', 'event']

def table_to_csv(table):
    stream = StringIO()
    table_writer = writer(stream, lineterminator='\n')
    table_writer.writerows(table)
    return stream.getvalue().strip()


def jsons_to_csv(json_lines_text, fieldnames, is_write_header = True):
    json_texts = json_lines_text.splitlines()
    table = []
    for json_text in json_texts:
        try:
            blob = loads(json_text)
            row = [blob[fieldname] for fieldname in fieldnames]
            table.append(row)
        except:
            print('Invalid for keys %r with JSON %r' % (
                fieldnames, json_text))
    table.sort()
    if is_write_header:
        table.insert(0, fieldnames)
    return table_to_csv(table)


def jsons_to_csv_file(json_paths, csv_path, fieldnames):
    header_text = jsons_to_csv('', fieldnames)
    with open(csv_path, 'w') as csv_file:
        csv_file.write(header_text)
    for json_path in json_paths:
        print('Parsing JSON to CSV in %r' % json_path)
        with open(json_path, 'r') as json_lines_file:
            json_lines_text = json_lines_file.read()
            csv_text = jsons_to_csv(json_lines_text, fieldnames, is_write_header = False)
        with open(csv_path, 'a') as csv_file:
            csv_file.write('\n' + csv_text)


if '__main__' == __name__:
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--fieldnames', nargs='*',
        default=fieldnames, help='Fieldnames to extract.')
    parser.add_argument('csv_path', help='Where to write CSV.')
    parser.add_argument('json_paths', nargs='*', help='File paths to JSON source.')
    args = parser.parse_args()
    if args.csv_path and args.json_paths:
        jsons_to_csv_file(args.json_paths, args.csv_path, args.fieldnames)
    from doctest import testfile
    testfile('README.md')
