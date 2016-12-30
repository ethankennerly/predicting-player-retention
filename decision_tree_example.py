"""
Copied from
http://scikit-learn.org/stable/modules/tree.html
"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from retention import write_pdf


pdf_path = 'test/iris.pdf'


iris = load_iris()
classifier = DecisionTreeClassifier()
classifier = classifier.fit(iris.data, iris.target)
probability_in_classes = classifier.predict_proba(iris.data[:1, :])
print('Probability first iris is in each class of irises: %r' % probability_in_classes)

write_pdf(classifier, pdf_path)
