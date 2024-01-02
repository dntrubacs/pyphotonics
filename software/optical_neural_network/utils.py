import numpy as np


def find_coordinate_matrix(n_size: int, n_length: float,
                           z_coordinate: float) -> np.ndarray:
    """ Find the position coordinates of elements in a physical representation
    of an n_size x n_size matrix located at position z.

    Keep in mind that the position of the elements is always considered to be
    in the middle. For example, if n_length=1, the element in the matrix at
    position [1, 2] will have coordinates [1+1/2, 2+1/2].

    Args:
        n_size: Size of the matrix (there will be n_size x n_size elements in
            the matrix).
        n_length: Length of the physical matrix (squared).
        z_coordinate: Z coordinate where the physical matrix is placed.

    Returns:
        Numpy array containing the coordinates of elements (n_size, n_size, 3)
        where the last entry represents: (x, y, z).
    """
    # the matrix containing all coordinates
    matrix = np.zeros(shape=(n_size, n_size, 3))

    # length of one pixel (or physical element of the matrix)
    pixel_length = n_length/n_size

    # go through each element in the matrix and assign its value
    for i in range(n_size):
        for j in range(n_size):
            matrix[i][j] = np.array([pixel_length*(i+0.5),
                                     pixel_length*(j+0.5),
                                     z_coordinate])

    return matrix


if __name__ == '__main__':
    # used only for testing and debugging
    debug_matrix = find_coordinate_matrix(n_size=4, n_length=0.5,
                                          z_coordinate=1)
    print(debug_matrix)
