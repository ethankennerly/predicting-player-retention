#!/bin/bash

## python retention.py data/part-00000.csv
## python retention.py --filter_path data/part-00000.training.csv --sample_percent 80 data/part-00000.csv
## python retention.py --filter_path data/part-00000.small.csv --sample_percent 96 data/part-00000.csv
python retention.py --aggregate_path data/part-00000.user.csv data/part-00000.csv
