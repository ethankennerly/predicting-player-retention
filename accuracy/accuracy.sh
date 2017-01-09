#!/bin/bash

echo "accuracy.sh expects MatMat answers data.  See README.md"
python accuracy.py --aggregate_path data/student_answers.csv data/answers.csv
python accuracy.py --plot data/student_answers.csv --classifier_index 0
python accuracy.py --plot data/student_answers.csv --classifier_index 1
python accuracy.py --plot data/student_answers.csv --classifier_index 2
python accuracy.py --plot data/student_answers.csv --classifier_index 3
python accuracy.py --plot data/student_answers.csv --classifier_index 4
python accuracy.py --plot data/student_answers.csv --classifier_index 5
python accuracy.py --plot data/student_answers.csv --classifier_index 6
python accuracy.py --plot data/student_answers.csv --classifier_index 7
python accuracy.py --plot data/student_answers.csv --classifier_index 8
python accuracy.py --plot data/student_answers.csv --classifier_index 9
