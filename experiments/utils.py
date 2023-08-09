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
    given in a lawnmower pattern starting from  [0,0].

    Args:
        n_pixels: Number of pixels on side of the square. Keep in
            mind the actual total number of pixels will be n_pixels**2.
        pixel_length: The length of a pixel (the length side of the
            pixel).

    Returns:
        2D numpy array representing the coordinates of the centre of each
        pixel in the square [pixel_number, [ x_coordinate, y_coordinates]].
    """
    # create a numpy array representing the square of the pixels
    # the last channel represent the x-y coordinates and the
    # pixel number (from 0 to n_pixels**2-1)
    square_pixels = np.zeros((n_pixels, n_pixels, 3))

    # set the value of each pixel in the array to the physical centre of the
    pixel_number = 0
    for i in range(n_pixels):
        # number the pixels from [0, 0] in lawnmower pattern
        if i % 2 == 0:
            for j in range(n_pixels):
                square_pixels[i][j] = [(2*i+1)*pixel_length/2,
                                       (2*j+1)*pixel_length/2,
                                       pixel_number]
                pixel_number += 1
        else:
            for j in range(n_pixels):
                square_pixels[i][j] = [(2*i+1)*pixel_length/2,
                                       (2*(n_pixels-j)-1)*pixel_length/2,
                                       pixel_number]
                pixel_number += 1

    # the coordinates assembled in the lawnmower pattern
    pattern = np.zeros((n_pixels**2, 2))
    for i in range(n_pixels):
        for j in range(n_pixels):
            pixel_number = int(square_pixels[i][j][2])

            # the x coordinates in the pattern for each pixel
            pattern[pixel_number][0] = square_pixels[i][j][0]

            # the y coordinates in the pattern for each pixel
            pattern[pixel_number][1] = square_pixels[i][j][1]

    # return the pattern
    return pattern


if __name__ == '__main__':
    # used only for testing and debugging
    debug_pattern = get_square_pattern(n_pixels=3, pixel_length=1)
    plt.figure(figsize=(12, 8))

    # set the limits
    plt.xlim([0, 3])
    plt.ylim([0, 3])

    # show the pixel grid
    for k in range(3):
        plt.vlines(x=k, ymin=0, ymax=3, color='black')
        plt.hlines(y=k, xmin=0, xmax=3, color='black')

    # show the pixel centers and their order
    debug_pixel_number = 0
    for point in debug_pattern:
        plt.plot(point[0], point[1], marker='o', markersize=10,
                 color='blue')
        plt.text(point[0], point[1], str(debug_pixel_number))
        debug_pixel_number += 1
    plt.show()
