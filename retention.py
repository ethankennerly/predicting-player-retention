"""
See README.md
"""


from json import loads
from StringIO import StringIO
from csv import writer


def jsons_to_csv(json_lines_text, fieldnames):
    json_texts = json_lines_text.splitlines()
    stream = StringIO()
    table_writer = writer(stream, lineterminator='\n')
    table_writer.writerow(fieldnames)
    for json_text in json_texts:
        try:
            blob = loads(json_text)
            row = [blob[fieldname] for fieldname in fieldnames]
            table_writer.writerow(row)
        except:
            print('Invalid for keys %r with JSON %r' % (
                fieldnames, json_text))
    return stream.getvalue().strip()


if '__main__' == __name__:
    from doctest import testfile
    testfile('README.md')
