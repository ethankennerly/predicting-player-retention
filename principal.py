"""
Adapted from
https://www.analyticsvidhya.com/blog/2016/03/practical-guide-principal-component-analysis-python/
"""

from numpy import cumsum, round
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale


def explains(features):
    scaled_features = scale(features)
    feature_count = len(features[0])
    analyzer = PCA(n_components = feature_count)
    analyzer.fit(scaled_features)
    variance_explained = cumsum(round(analyzer.explained_variance_ratio_, decimals = 3))
    return variance_explained


def explains_text(features):
    text = 'Cumulative variance explained with number of components:\n'
    text += str(explains(features))
    return text


def principal_components(features, component_count):
    analyzer = PCA(n_components = component_count)
    scaled_features = scale(features)
    analyzer.fit(scaled_features)
    components = analyzer.fit_transform(scaled_features)
    return components
