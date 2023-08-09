"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 9 August 2023. The
purpose of this module is to create certain utilities functions to help
with the running of the experiments.
"""

from matplotlib import pyplot as plt
import numpy as np


def get_square_pattern(n_pixels: int = 3, pixel_length: float = 1.0) \
        -> np.ndarray:
    """ Gets the pattern followed by the motors to build a squared made of
    multiple pixels.

    The pattern represents the coordinates of the centre of each pixel
    given in a lawnmower pattern starting from top left (always [0,0])
    to bottom right.

    Args:
        n_pixels: Number of pixels on side of the square. Keep in
            mind the actual total number of pixels will be n_pixels**2.
        pixel_length: The length of a pixel (the length side of the
            pixel).

    Returns:
        2D numpy array representing the coordinates of the centre of each
        pixel in the square [x_coordinates, y_coordinates].
    """
