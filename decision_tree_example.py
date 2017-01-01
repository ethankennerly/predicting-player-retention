"""
Copied from:
http://scikit-learn.org/stable/modules/tree.html
http://scikit-learn.org/stable/modules/cross_validation.html

elyase explained random_state:
http://stackoverflow.com/questions/28064634/random-state-pseudo-random-numberin-scikit-learn
"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from retention import fit_score, write_pdf


pdf_path = 'test/iris.pdf'

iris = load_iris()

classifier = DecisionTreeClassifier()
classifier, score = fit_score(classifier, iris.data, iris.target)
print('Decision tree score: %0.2f' % score)
probability_in_classes = classifier.predict_proba(iris.data[:1, :])
print('Probability first iris is in each class of irises: %r' % probability_in_classes)

write_pdf(classifier, pdf_path)
