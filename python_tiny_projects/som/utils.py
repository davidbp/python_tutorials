import numpy as np

def sqeuclidean(x_mat: 'np.ndarray', y_mat: 'np.ndarray') -> 'np.ndarray':
    """squared Euclidean distance between each row in x_mat and each row in y_mat.
    :param x_mat: np.ndarray with ndim=2
    :param y_mat: np.ndarray with ndim=2
    :return: np.ndarray with ndim=2
    """
    return (
        np.sum(y_mat ** 2, axis=1)
        + np.sum(x_mat ** 2, axis=1)[:, np.newaxis]
        - 2 * np.dot(x_mat, y_mat.T)
    )


def euclidean(x_mat: 'np.ndarray', y_mat: 'np.ndarray') -> 'np.ndarray':
    """squared Euclidean distance between each row in x_mat and each row in y_mat.
    :param x_mat: np.ndarray with ndim=2
    :param y_mat: np.ndarray with ndim=2
    :return: np.ndarray with ndim=2
    """
    return np.sqrt(
        np.sum(y_mat ** 2, axis=1)
        + np.sum(x_mat ** 2, axis=1)[:, np.newaxis]
        - 2 * np.dot(x_mat, y_mat.T)
    )


