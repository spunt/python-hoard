import numpy as np
standarize_minmax(self, x, x_min, x_max):
        return ( 2*x - x_max - x_min ) / ( x_max - x_min )


def rescale(X):
    """Rescale data between [0, 1]"""
    numer = X - np.min(X)
    denom = np.max(X) - np.min(X)
    return numer / denom


def mean_normalize(X):
    """Normalize the mean of a given distribution"""
    numer = X - np.mean(X)
    denom = np.max(X) - np.min(X)
    return numer / denom


def standardize(X):
    """Standardize features to have zero mean and unit-variance"""
    # X - X_bar / std
    x_bar = np.mean(X)  # feature means
    sigma = np.std(X)  # feature st deviations
    return (X - x_bar) / sigma
# RESCALE:
(Z - Z.min())/(Z.max() - Z.min())



# Standardize a feature

# Load libraries
from sklearn import preprocessing
import numpy as np

# Create feature
x = np.array([[-500.5],
              [-100.1],
              [0],
              [100.1],
              [900.9]])
# Standardize Feature
# Create scaler
scaler = preprocessing.StandardScaler()

# Transform the feature
standardized = scaler.fit_transform(x)

# Show feature
standardizedSt

# Standardize dataset
import numpy as np

def standardize(x):
    """Standardize the original data set."""

    # get the vector of means (for each feature)
    mean_x = np.mean(x, axis = 0)

    # pair wise substraction of those means in each feature space
    x = x - mean_x

    # get the vector of standard deviations (for each feature)
    std_x = np.std(x, axis = 0)

    # pair wise division of those standard deviations in each feature space
    x = x / std_x

    return x, mean_x, std_x



"""Functions for feature scaling."""

def normalize(X):
    """Normalize features X (min-max-scaling).
    Args:
        X: Feature set to scale.
    Returns:
        Min-max-scaled feature set.
    """
    min_ = X.min(axis=0)
    max_ = X.max(axis=0)

    return (X - min_) / (max_ - min_)

def standardize(X):
    """Standardize feature set X.
    Args:
        X: Feature set to scale.
    Returns:
        Scaled feature set.
    """
    mean = X.mean(axis=0)
    variance = X.var(axis=0)

    return (X - mean) / variance
