#!/bin/bash

## python retention.py --filter_path test/part-00000.small.csv --sample_percent 96 data/part-00000.csv
python retention.py --aggregate_path test/part-00000.small.csv.test.user.csv test/part-00000.small.csv.test.csv
python retention.py --plot test/part-00000.small.csv.test.user.csv
