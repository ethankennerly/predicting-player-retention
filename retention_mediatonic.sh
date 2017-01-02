#!/bin/bash

echo "retention_mediatonic.sh expects tabulated Mediatonic workshop data.  See README.md"
# python retention.py --aggregate_path data/part-00000.user.csv data/part-00000.csv
python retention.py --plot data/part-00000.user.csv
