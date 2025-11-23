import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing, load_iris, make_regression, make_blobs

def get_housing_data():
    """
    Fetches California housing data and returns a pandas DataFrame.
    """
    data = fetch_california_housing()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Target_Price'] = data.target
    return df

def get_iris_data():
    """
    Fetches Iris dataset and returns a pandas DataFrame.
    """
    data = load_iris()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Species'] = pd.Categorical.from_codes(data.target, data.target_names)
    return df

def generate_random_data(rows=100, cols=3):
    """
    Generates a random dataframe.
    """
    data = np.random.randn(rows, cols)
    columns = [f"Col_{i+1}" for i in range(cols)]
    return pd.DataFrame(data, columns=columns)

def generate_linear_data(n_samples=100, noise=10.0, slope=2.0):
    """
    Generates synthetic linear regression data.
    """
    X = np.random.rand(n_samples) * 10
    y = slope * X + np.random.randn(n_samples) * noise
    return pd.DataFrame({'X': X, 'y': y})
