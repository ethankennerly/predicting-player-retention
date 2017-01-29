#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
=====================
Classifier comparison
=====================

A comparison of a several classifiers in scikit-learn on synthetic datasets.
The point of this example is to illustrate the nature of decision boundaries
of different classifiers.
This should be taken with a grain of salt, as the intuition conveyed by
these examples does not necessarily carry over to real datasets.

Particularly in high-dimensional spaces, data can more easily be separated
linearly and the simplicity of classifiers such as naive Bayes and linear SVMs
might lead to better generalization than is achieved by other classifiers.

The plots show training points in solid colors and testing points
semi-transparent. The lower right shows the classification accuracy on the test
set.
"""


# Code source: Gaël Varoquaux
#              Andreas Müller
# Modified for documentation by Jaques Grobler
# Extracted plot function to reuse with a novel dataset by Ethan Kennerly
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


def moon_circle_line_datasets():
    X, y = make_classification(n_features=2, n_redundant=0, n_informative=2,
                               random_state=1, n_clusters_per_class=1)
    rng = np.random.RandomState(2)
    X += 2 * rng.uniform(size=X.shape)
    linearly_separable = (X, y)
    datasets = [make_moons(noise=0.3, random_state=0),
                make_circles(noise=0.2, factor=0.5, random_state=1),
                linearly_separable
                ]
    return datasets


def sample_classifiers():
    names = [
        "Decision Tree",
        "Nearest Neighbors",
        "Random Forest",
    ]
    classifiers = [
        DecisionTreeClassifier(max_depth=5),
        KNeighborsClassifier(3),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    ]
    return names, classifiers


def all_classifiers():
    max_depth = 5
    names = [
        "Decision Tree",
        "Nearest Neighbors",
        "Gaussian Process",
        "Random Forest",
        "QDA",
        "Neural Net",
        "RBF SVM",
        "Naive Bayes",
        "Linear SVM",
        "AdaBoost",
    ]
    classifiers = [
        DecisionTreeClassifier(max_depth=max_depth),
        KNeighborsClassifier(3),
        GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
        RandomForestClassifier(max_depth=max_depth, n_estimators=10, max_features=1),
        QuadraticDiscriminantAnalysis(),
        MLPClassifier(alpha=1),
        SVC(kernel="linear", C=0.025, decision_function_shape='ovr'),
        GaussianNB(),
        SVC(gamma=2, C=1, decision_function_shape='ovr'),
        AdaBoostClassifier(),
    ]
    return names, classifiers


def plot_comparison(datasets, names = None, classifiers = None, is_verbose=False, output_path=None):
    if not names and not classifiers:
        names, classifiers = all_classifiers()
    h = .02  # step size in the mesh
    cell_size = 3
    width = cell_size * (len(classifiers) + 1)
    height = cell_size * len(datasets)
    figure = plt.figure(figsize=(width, height))
    i = 1
    # iterate over datasets
    for ds_cnt, ds in enumerate(datasets):
        # preprocess dataset, split into training and test part
        X, y = ds
        X = StandardScaler().fit_transform(X)
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=.4, random_state=42)
        if is_verbose:
            print('plot_classifier_comparison: index %r size %r head %r' % (
                ds_cnt, X_train.size, X_train[:2]))
        feature_count = X.shape[1]
        second_index = min(2, feature_count - 1)
        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, second_index].min() - .5, X[:, second_index].max() + .5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        # just plot the dataset first
        cm = plt.cm.RdBu
        cm_bright = ListedColormap(['#FF0000', '#0000FF'])
        ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
        if ds_cnt == 0:
            ax.set_title("Input data")
        # Plot the training points
        ax.scatter(X_train[:, 0], X_train[:, second_index], c=y_train, cmap=cm_bright)
        # and testing points
        ax.scatter(X_test[:, 0], X_test[:, second_index], c=y_test, cmap=cm_bright, alpha=0.6)
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())
        i += 1

        # iterate over classifiers
        for name, clf in zip(names, classifiers):
            ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)

            # Plot the decision boundary. For that, we will assign a color to each
            # point in the mesh [x_min, x_max]x[y_min, y_max].
            if 2 <= feature_count:
                mesh = np.c_[xx.ravel(), yy.ravel()]
            else:
                mesh = np.c_[xx.ravel()]
            if hasattr(clf, "decision_function"):
                Z = clf.decision_function(mesh)
            else:
                Z = clf.predict_proba(mesh)
                Z = Z[:, 1]
            # Put the result into a color plot
            if is_verbose:
                print('name %r Z.shape %r xx.shape %r size ratio %r Z head %r' % (
                    name, Z.shape, xx.shape, float(Z.size) / xx.size, Z[:2]))
            Z = Z.reshape(xx.shape)
            ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)

            # Plot also the training points
            ax.scatter(X_train[:, 0], X_train[:, second_index], c=y_train, cmap=cm_bright)
            # and testing points
            ax.scatter(X_test[:, 0], X_test[:, second_index], c=y_test, cmap=cm_bright,
                       alpha=0.6)

            ax.set_xlim(xx.min(), xx.max())
            ax.set_ylim(yy.min(), yy.max())
            ax.set_xticks(())
            ax.set_yticks(())
            if ds_cnt == 0:
                ax.set_title(name)
            ax.text(xx.max() - .3, yy.min() + .3, ('%.2f' % score).lstrip('0'),
                    size=15, horizontalalignment='right')
            i += 1
    plt.tight_layout()
    if output_path:
        print('plot_comparison: Saved figure to: %r' % output_path)
        figure.savefig(output_path)
        plt.close(figure)
    else:
        plt.show()


if '__main__' == __name__:
    print(__doc__)
    datasets = moon_circle_line_datasets()
    plot_comparison(datasets)
