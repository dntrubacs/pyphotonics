"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 9 August 2023. The
purpose of this module is to create certain utilities functions to help
with the running of the experiments.

Last update: 11 August 2023
"""

from matplotlib import pyplot as plt
import numpy as np


def plot_pixel_pattern(pattern: np.ndarray | list, title: str,
                       start_pixel: np.ndarray | list, n_pixels: int,
                       pixel_length: float) -> None:
    """ Plots a pixel pattern.

    Args:
        pattern: Numpy array representing the position of each pixel
        title: The title of the figure.
        start_pixel: The pixel from where the plot will start (bottom left).
        n_pixels: The number of pixels shown in the plot.
        pixel_length: The size of each pixel.
    """
    # create the figure
    plt.figure(figsize=(12, 8))
    plt.title(title)
    plt.xlabel('X position (mm)')
    plt.ylabel("Y position (mm)")

    # set the limits
    plt.xlim([start_pixel[0], pixel_length * n_pixels + start_pixel[0]])
    plt.ylim([start_pixel[1], pixel_length * n_pixels + start_pixel[1]])

    # show the pixel grid
    for n_grid in range(n_pixels):
        plt.vlines(x=pixel_length * n_grid + start_pixel[0],
                   ymin=start_pixel[1],
                   ymax=pixel_length * n_pixels + start_pixel[1],
                   color='black')

        plt.hlines(y=pixel_length * n_grid + start_pixel[1],
                   xmin=start_pixel[0],
                   xmax=pixel_length * n_pixels + start_pixel[0],
                   color='black')

        # show the pixel centers and their order
        pixel_number = 0
        for point in pattern:
            plt.plot(point[0], point[1], marker='o', markersize=15,
                     color='blue')
            plt.text(point[0], point[1], str(pixel_number), size=15)
            pixel_number += 1

    # show the pattern
    plt.show()


def get_horizontal_pattern(start_pixel: np.ndarray | list, n_pixels: int = 3,
                           pixel_length: float = 1.0,
                           direction: int = 1) -> np.ndarray:
    """ Gets the pattern of a horizontal line that starts from a given pixel.

    Args:
        start_pixel: Coordinates of the pixel [x_coordinate, y_coordinates]
            representing the place from where to start the pattern.
        n_pixels: Number of pixels on side of the square. Keep in
            mind the actual total number of pixels will be n_pixels**2.
        pixel_length: The length of a pixel (the length side of the
            pixel).
        direction: Whether to go in the +x direction (+1) or in the -x
            direction (-1).

    Returns:
        2D numpy array (n_pixels**2, 2) representing the coordinates of the
        centre of each pixel in the horizontal line pattern.
    """
    # the horizontal pattern
    pattern = np.zeros((n_pixels, 2))

    # go through each point in the pattern and change it according to direction
    for i in range(n_pixels):
        pattern[i][0] += direction * pixel_length * i + start_pixel[0]
        pattern[i][1] = start_pixel[1]

    # return the pattern
    return pattern


def get_vertical_pattern(start_pixel: np.ndarray | list, n_pixels: int = 3,
                         pixel_length: float = 1.0,
                         direction: int = 1) -> np.ndarray:
    """ Gets the pattern of a vertical line that starts from a given pixel.

    Args:
        start_pixel: Coordinates of the pixel [x_coordinate, y_coordinates]
            representing the place from where to start the pattern.
        n_pixels: Number of pixels on side of the square. Keep in
            mind the actual total number of pixels will be n_pixels**2.
        pixel_length: The length of a pixel (the length side of the
            pixel).
        direction: Whether to go in the +x direction (+1) or in the -x
            direction (-1).

    Returns:
        2D numpy array (n_pixels**2, 2) representing the coordinates of the
        centre of each pixel in the vertical line pattern.
    """
    # the horizontal pattern
    pattern = np.zeros((n_pixels, 2))

    # go through each point in the pattern and change it according to direction
    for i in range(n_pixels):
        pattern[i][0] = start_pixel[0]
        pattern[i][1] += direction * pixel_length * i + start_pixel[1]

    # return the pattern
    return pattern


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


def get_s_pattern(start_pixel: np.ndarray | list, n_pixels: int = 3,
                  pixel_length: float = 1.0) -> np.ndarray:
    """ Get the pattern representing the S letter.

    start_pixel: Coordinates of the pixel [x_coordinate, y_coordinates]
            representing the place from where to start the pattern.
        n_pixels: Number of pixels of the side of the letter.
        pixel_length: The length of a pixel (the length side of the
            pixel).

    Returns:
        2D numpy array (n_pixels**2, 2) representing the coordinates of the
        centre of each pixel in the S letter pattern.
    """
    # get the bottom line of S
    s_pattern = get_horizontal_pattern(start_pixel=start_pixel,
                                       n_pixels=n_pixels,
                                       pixel_length=pixel_length,
                                       direction=1)

    # get the right vertical line of S
    pattern = get_vertical_pattern(start_pixel=s_pattern[-1],
                                   n_pixels=n_pixels,
                                   pixel_length=pixel_length,
                                   direction=1)
    s_pattern = np.concatenate((s_pattern, pattern))

    # get the middle horizontal line
    pattern = get_horizontal_pattern(start_pixel=s_pattern[-1],
                                     n_pixels=n_pixels,
                                     pixel_length=pixel_length,
                                     direction=-1)
    s_pattern = np.concatenate((s_pattern, pattern))

    # get the left vertical line of S
    pattern = get_vertical_pattern(start_pixel=s_pattern[-1],
                                   n_pixels=n_pixels,
                                   pixel_length=pixel_length,
                                   direction=1)
    s_pattern = np.concatenate((s_pattern, pattern))

    # get the up horizontal line
    pattern = get_horizontal_pattern(start_pixel=s_pattern[-1],
                                     n_pixels=n_pixels,
                                     pixel_length=pixel_length,
                                     direction=1)
    s_pattern = np.concatenate((s_pattern, pattern))

    # return the s_pattern found
    return s_pattern


def get_o_pattern(start_pixel: np.ndarray | list, n_pixels_width: int = 3,
                  n_pixels_height: int = 3,
                  pixel_length: float = 1.0) -> np.ndarray:
    """ Get the pattern representing the O letter.

    start_pixel: Coordinates of the pixel [x_coordinate, y_coordinates]
            representing the place from where to start the pattern.
        n_pixels_width: Number of pixels representing the width of the letter.
        n_pixels_height: Number of pixels representing the height of the
            letter.
        pixel_length: The length of a pixel (the length side of the
            pixel).

    Returns:
        2D numpy array (n_pixels**2, 2) representing the coordinates of the
        centre of each pixel in the O letter pattern.
    """
    # get the bottom line of S
    o_pattern = get_horizontal_pattern(start_pixel=start_pixel,
                                       n_pixels=n_pixels_width,
                                       pixel_length=pixel_length,
                                       direction=1)

    # get the right vertical line of O
    pattern = get_vertical_pattern(start_pixel=o_pattern[-1],
                                   n_pixels=n_pixels_height,
                                   pixel_length=pixel_length,
                                   direction=1)
    o_pattern = np.concatenate((o_pattern, pattern))

    # get the up horizontal line
    pattern = get_horizontal_pattern(start_pixel=o_pattern[-1],
                                     n_pixels=n_pixels_width,
                                     pixel_length=pixel_length,
                                     direction=-1)
    o_pattern = np.concatenate((o_pattern, pattern))

    # get the left vertical line of O
    pattern = get_vertical_pattern(start_pixel=o_pattern[-1],
                                   n_pixels=n_pixels_height,
                                   pixel_length=pixel_length,
                                   direction=-1)
    o_pattern = np.concatenate((o_pattern, pattern))

    # return the s_pattern found
    return o_pattern


def get_t_pattern(start_pixel: np.ndarray | list, n_pixels_width: int = 3,
                  n_pixels_height: int = 3,
                  pixel_length: float = 1.0) -> np.ndarray:
    """ Get the pattern representing the T letter.

    start_pixel: Coordinates of the pixel [x_coordinate, y_coordinates]
            representing the place from where to start the pattern.
        n_pixels_width: Number of pixels representing the width of the letter
            (must be odd).
        n_pixels_height: Number of pixels representing the height of the
            letter.
        pixel_length: The length of a pixel (the length side of the
            pixel).

    Returns:
        2D numpy array (n_pixels**2, 2) representing the coordinates of the
        centre of each pixel in the T letter pattern.
    """
    # get the vertical line of T
    t_pattern = get_vertical_pattern(start_pixel=start_pixel,
                                     n_pixels=n_pixels_height,
                                     pixel_length=pixel_length,
                                     direction=1)

    # get the right horizontal line of T
    left_pattern = get_horizontal_pattern(
        start_pixel=t_pattern[-1],
        n_pixels=int(n_pixels_width / 2) + 1,
        pixel_length=pixel_length,
        direction=-1)

    right_pattern = get_horizontal_pattern(
        start_pixel=t_pattern[-1],
        n_pixels=int(n_pixels_width / 2) + 1,
        pixel_length=pixel_length,
        direction=1)
    t_pattern = np.concatenate((t_pattern, left_pattern))
    t_pattern = np.concatenate((t_pattern, right_pattern))

    # return the t_pattern found
    return t_pattern


def get_n_pattern(start_pixel: np.ndarray | list, n_pixels_width: int = 3,
                  n_pixels_height: int = 3,
                  pixel_length: float = 1.0) -> np.ndarray:
    """ Get the pattern representing the N letter.

        start_pixel: Coordinates of the pixel [x_coordinate, y_coordinates]
            representing the place from where to start the pattern.
        n_pixels_width: Number of pixels representing the width of the letter
            (must be odd).
        n_pixels_height: Number of pixels representing the height of the
            letter.
        pixel_length: The length of a pixel (the length side of the
            pixel).

    Returns:
        2D numpy array (n_pixels**2, 2) representing the coordinates of the
        centre of each pixel in the N letter pattern.
    """
    # get the left vertical line of N
    n_pattern = get_vertical_pattern(start_pixel=start_pixel,
                                     n_pixels=n_pixels_height,
                                     pixel_length=pixel_length,
                                     direction=1)

    # get the diagonal points between the two vertical lines of N
    for n in range(int(n_pixels_width/2)):
        diagonal_point = n_pattern[-1] + [pixel_length, -pixel_length]
        diagonal_point = np.reshape(a=diagonal_point,
                                    newshape=(1, 2))
        n_pattern = np.concatenate((n_pattern, diagonal_point))

    # get the right vertical line of T
    pattern = get_vertical_pattern(
        start_pixel=start_pixel + [(n_pixels_width-1)*pixel_length, 0],
        n_pixels=n_pixels_height,
        pixel_length=pixel_length,
        direction=1)
    n_pattern = np.concatenate((n_pattern, pattern))

    # return the t_pattern found
    return n_pattern


def get_soton_pattern(start_pixel: np.ndarray | list,
                      pixel_length: float) -> np.ndarray:
    """ Get the SOTON pattern being written in pixels. The size of all
    letters is 3x5 (except N which is 4x5)

    Args:
        start_pixel: Coordinates of the pixel [x_coordinate, y_coordinates]
            representing the place from where to start the pattern.
        pixel_length: The length of a pixel (the length side of the
            pixel).

    Returns: 2D numpy array (n_pixels**2, 2) representing the coordinates of the
        centre of each pixel in the SOTON pattern.
    """
    # get the pattern of letter S
    soton_pattern = get_s_pattern(start_pixel=start_pixel,
                                  pixel_length=pixel_length,
                                  n_pixels=3)

    # get the pattern of letter O
    o_pattern = get_o_pattern(start_pixel=start_pixel + [pixel_length*3, 0],
                              pixel_length=pixel_length,
                              n_pixels_height=5,
                              n_pixels_width=3)
    soton_pattern = np.concatenate((soton_pattern, o_pattern))

    # get the pattern of letter T
    t_pattern = get_t_pattern(start_pixel=start_pixel + [pixel_length * 7, 0],
                              pixel_length=pixel_length,
                              n_pixels_height=5,
                              n_pixels_width=3)
    soton_pattern = np.concatenate((soton_pattern, t_pattern))

    # get the pattern of letter O
    o_pattern = get_o_pattern(start_pixel=start_pixel + [pixel_length * 9, 0],
                              pixel_length=pixel_length,
                              n_pixels_height=5,
                              n_pixels_width=3)
    soton_pattern = np.concatenate((soton_pattern, o_pattern))

    # get the pattern of letter N
    n_pattern = get_n_pattern(start_pixel=start_pixel + [pixel_length * 12, 0],
                              pixel_length=pixel_length,
                              n_pixels_height=5,
                              n_pixels_width=4)
    soton_pattern = np.concatenate((soton_pattern, n_pattern))

    # return the SOTON pattern found
    return soton_pattern

if __name__ == '__main__':
    # used only for testing and debugging
    debug_start_pixel = np.array([0.5152478134110787, 5.314402332361516])
    debug_n_pixels = 3
    debug_pixel_length = 4E-6
    debug_pattern = get_soton_pattern(
        start_pixel=debug_start_pixel + [debug_pixel_length, 0],
        pixel_length=debug_pixel_length)
    for i in range(debug_pattern.shape[0]):
        print(i, debug_pattern[i])

    # start pixel for plotting
    debug_start_pixel_plot = debug_start_pixel - debug_pixel_length / 2

    # the numbers of pixels used for plotting
    debug_n_pixels_plot = 21

    # show a figure of the pixels arranged in a lawnmower pattern
    plot_pixel_pattern(pattern=debug_pattern,
                       start_pixel=debug_start_pixel_plot,
                       pixel_length=debug_pixel_length,
                       n_pixels=debug_n_pixels_plot,
                       title='Pixels arranged in a lawnmower pattern')
