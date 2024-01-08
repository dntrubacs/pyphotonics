""" Created by Daniel-Iosif Trubacs on 2 January 2024 for the UoS Integrated
Nanophotonics Group. The purpose of this module is to create certain utils
function that will help with the processing of datasets.
"""

import numpy as np
from matplotlib import pyplot as plt


def create_detector_from_label(label: int) -> np.ndarray:
    """ Creates a detector of size 10 x 10 that corresponds to a given number

    The label used in diffractive neural networks (the last layer) for
    the mnist dataset represents a detector with multiple regions where each
    region corresponds to a given number.
    """
    # initialize the detector array as 0
    detector_array = np.zeros(shape=(10, 10))

    if label == 0:
        detector_array[1][8] = 1
        detector_array[1][7] = 1
        detector_array[2][8] = 1
        detector_array[2][7] = 1

    if label == 1:
        detector_array[3][8] = 1
        detector_array[3][7] = 1
        detector_array[4][8] = 1
        detector_array[4][7] = 1

    if label == 2:
        detector_array[5][8] = 1
        detector_array[5][7] = 1
        detector_array[6][8] = 1
        detector_array[6][7] = 1

    if label == 3:
        detector_array[7][8] = 1
        detector_array[7][7] = 1
        detector_array[8][8] = 1
        detector_array[8][7] = 1

    if label == 4:
        detector_array[1][5] = 1
        detector_array[2][5] = 1
        detector_array[1][4] = 1
        detector_array[2][4] = 1

    if label == 5:
        detector_array[4][5] = 1
        detector_array[5][5] = 1
        detector_array[4][4] = 1
        detector_array[5][4] = 1

    if label == 6:
        detector_array[7][5] = 1
        detector_array[8][5] = 1
        detector_array[7][4] = 1
        detector_array[8][4] = 1

    if label == 7:
        detector_array[1][2] = 1
        detector_array[2][2] = 1
        detector_array[1][1] = 1
        detector_array[2][1] = 1

    if label == 8:
        detector_array[4][2] = 1
        detector_array[5][2] = 1
        detector_array[4][1] = 1
        detector_array[5][1] = 1

    if label == 9:
        detector_array[7][2] = 1
        detector_array[8][2] = 1
        detector_array[7][1] = 1
        detector_array[8][1] = 1

    return detector_array


if __name__ == '__main__':
    debug_detector = create_detector_from_label(label=9)
    plt.imshow(debug_detector.T, origin='lower')
    plt.show()