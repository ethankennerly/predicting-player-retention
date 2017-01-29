#!/bin/bash

echo "accuracy.sh expects MatMat answers data.  See README.md"
answer_count=10
feature_count=8
python accuracy.py --answer_count $answer_count --aggregate_path data/student_answers.csv data/answers.csv
python accuracy.py --answer_count $answer_count --summarize data/student_answers.csv
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 0
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 1
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 2
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 3
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 4
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 5
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 6
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 7
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 8
python accuracy.py --feature_count $feature_count --pca --answer_count $answer_count --plot data/student_answers.csv --classifier_index 9
