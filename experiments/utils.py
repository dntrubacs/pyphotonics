"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 9 August 2023. The
purpose of this module is to create certain utilities functions to help
with the running of the experiments.

Last update: 11 August 2023
"""

from matplotlib import pyplot as plt
import numpy as np


def get_square_pattern(start_pixel: np.ndarray | list, n_pixels: int = 3,
                       pixel_length: float = 1.0) -> np.ndarray:
    """ Gets the pattern followed by the motors to build a squared made of
    multiple pixels.

    The pattern represents the coordinates of the centre of each pixel
    given in a lawnmower pattern starting from  [0,0].

    Args:
        start_pixel: Coordinates of the pixel [x_coordinate, y_coordinates]
            representing the place from where to start the pixel map
            (can be though of as bottom left of the pixel map).
        n_pixels: Number of pixels on side of the square. Keep in
            mind the actual total number of pixels will be n_pixels**2.
        pixel_length: The length of a pixel (the length side of the
            pixel).

    Returns:
        2D numpy array (n_pixels**2, 2) representing the coordinates of the
        centre of each pixel in the square listed in a lawnmower pattern.
    """
    # create a numpy array representing the square of the pixels (pixel_map)
    # the last channel represents the x-y coordinates and the
    # pixel number (from 0 to n_pixels**2-1)
    pixel_map = np.zeros((n_pixels, n_pixels, 3))

    # set the value of each pixel in the array to the physical centre of the
    pixel_number = 0
    for i in range(n_pixels):
        # number the pixels from start_pixel in lawnmower pattern
        if i % 2 == 0:
            for j in range(n_pixels):
                pixel_map[i][j] = [
                    (2 * i + 1) * pixel_length / 2 + start_pixel[0],
                    (2 * j + 1) * pixel_length / 2 + start_pixel[1],
                    pixel_number]
                pixel_number += 1
        else:
            for j in range(n_pixels):
                pixel_map[i][j] = [
                    (2 * i + 1) * pixel_length / 2 + start_pixel[0],
                    (2 * (n_pixels - j) - 1) * pixel_length / 2 +
                    start_pixel[1],
                    pixel_number]
                pixel_number += 1

    # add the star-pixel values to the pixel map
    print(pixel_map.shape, pixel_map[0][0])

    # the coordinates assembled in the lawnmower pattern
    pattern = np.zeros((n_pixels ** 2, 2))
    for i in range(n_pixels):
        for j in range(n_pixels):
            pixel_number = int(pixel_map[i][j][2])

            # the x coordinates in the pattern for each pixel
            pattern[pixel_number][0] = pixel_map[i][j][0]

            # the y coordinates in the pattern for each pixel
            pattern[pixel_number][1] = pixel_map[i][j][1]

    # return the pattern
    return pattern


if __name__ == '__main__':
    # used only for testing and debugging
    debug_start_pixel = [1, 1]
    debug_n_pixels = 3
    debug_pixel_length = 2e-6
    debug_pattern = get_square_pattern(start_pixel=debug_start_pixel,
                                       n_pixels=debug_n_pixels,
                                       pixel_length=debug_pixel_length)

    # show a figure of the pixels arranged in lawnmower pattern
    plt.figure(figsize=(12, 8))
    plt.title('Pixels of size 1 $\mu m$ arranged in a lawnmower pattern')

    # set the limits
    plt.xlim([debug_start_pixel[0], debug_pixel_length * debug_n_pixels +
              debug_start_pixel[0]])
    plt.ylim([debug_start_pixel[1], debug_pixel_length * debug_n_pixels +
              debug_start_pixel[1]])

    # show the pixel grid
    for k in range(debug_n_pixels):
        print(k)
        plt.vlines(x=debug_pixel_length * k + debug_start_pixel[0],
                   ymin=debug_start_pixel[1],
                   ymax=debug_pixel_length * debug_n_pixels +
                   debug_start_pixel[1], color='black')

        plt.hlines(y=debug_pixel_length * k + debug_start_pixel[1],
                   xmin=debug_start_pixel[0],
                   xmax=debug_pixel_length * debug_n_pixels +
                   debug_start_pixel[0], color='black')

    # show the pixel centers and their order
    debug_pixel_number = 0
    for point in debug_pattern:
        plt.plot(point[0], point[1], marker='o', markersize=10,
                 color='blue')
        plt.text(point[0], point[1], str(debug_pixel_number), size=15)
        debug_pixel_number += 1
    plt.show()
