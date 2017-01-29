"""
Extracted from plot_classifier_comparison.py
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from plot_classifier_comparison import all_classifiers


names, classifiers = all_classifiers()


def score(features, classes, classifier_index):
    scaled_features = StandardScaler().fit_transform(features)
    classifier = classifiers[classifier_index]
    X_train, X_test, y_train, y_test = \
        train_test_split(scaled_features, classes, test_size=.4, random_state=42)
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    score = round(score, 2)
    return score


def score_text(features, classes, classifier_index):
    name = names[classifier_index]
    accuracy = score(features, classes, classifier_index)
    feature_count = len(features[0])
    text = '%s features %s score %s' % (name, feature_count, accuracy)
    return text
