#!/bin/bash

## python retention.py --filter_path test/part-00000.small.csv --sample_percent 96 data/part-00000.csv
python retention.py --random_state 0 --aggregate_path test/part-00000.small.csv.test.user.csv test/part-00000.small.csv.test.csv
python retention.py --random_state 0 --plot test/part-00000.small.csv.test.user.csv
python retention.py --random_state 0 --plot test/part-00000.small.csv.test.user.csv --classifier_index 9
