#!/bin/bash

echo "retention_mediatonic.sh expects tabulated Mediatonic workshop data.  See README.md"
python retention.py --aggregate_path data/part-00000.user.csv data/part-00000.csv
python retention.py --plot data/part-00000.user.csv --classifier_index 0
python retention.py --plot data/part-00000.user.csv --classifier_index 1
python retention.py --plot data/part-00000.user.csv --classifier_index 2
python retention.py --plot data/part-00000.user.csv --classifier_index 3
python retention.py --plot data/part-00000.user.csv --classifier_index 4
python retention.py --plot data/part-00000.user.csv --classifier_index 5
python retention.py --plot data/part-00000.user.csv --classifier_index 6
python retention.py --plot data/part-00000.user.csv --classifier_index 7
python retention.py --plot data/part-00000.user.csv --classifier_index 8
python retention.py --plot data/part-00000.user.csv --classifier_index 9
