import numpy as np


def roll(a, b, dx=1, dy=1):
    shape = a.shape[:-2] + ((a.shape[-2] - b.shape[-2]) // dy + 1,) + ((a.shape[-1] - b.shape[-1]) // dx + 1,) + b.shape
    strides = a.strides[:-2] + (a.strides[-2] * dy,) + (a.strides[-1] * dx,) + a.strides[-2:]
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


print(roll(np.array([np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
                     np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
                     np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
                     np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
                     np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
                     np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),], dtype=object),
           np.array([[0 for _ in range(4)] for _ in range(4)])))
