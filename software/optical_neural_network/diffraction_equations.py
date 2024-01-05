"""
Created by Daniel-Iosif Trubacs on 3 January 2024 for the UoS Integrated
Nanophotonics Group. The purpose of this module is to create certain
diffraction equations based on the Rayleigh-Sommerfeld model. The equation
for the optical w at a position (x,y,z) generated from a source at position
(x_i, z_i, z_i) and wavelength lambda is:
w = (z-z_i)/r**2 * (1/(2*pi*r) + 1/(lambda*j))*exp(j*2*pi*r/lambda) (1)
  = factor*(inverse_distance + inverse_wavelength)*exponential_term

where r = sqrt((x-x_i)**2 + (y-y_i)**2 + (z-z_i)**2) and j is the imaginary
number sqrt(-1). If the calculation take into account the source optical
mode s (complex number representing amplitude and phase), then the optical
new optical mode n will simply be:
n = w*s

All the calculations are done using the torch backend as this integrates easier
with neural network architecture.

For more information about the mathematical algorithms behind the optical
neural network used please check the following References:

1. https://www.science.org/doi/10.1126/science.aat8084#supplementary-materials
"""


import torch
import math
from typing import Callable


def find_optical_mode(source_position: torch.tensor,
                      detector_position: torch.tensor,
                      source_optical_mode: torch.tensor,
                      wavelength: float) -> torch.tensor:
    """ Finds the optical mode at a given position from a given source.

    The output function is based on the
    Args:
        source_position: Torch tensor representing the coordinates of the
            source (x, y, z).
        detector_position: Torch tensor representing the coordinates of the
            of detector (x_i, y_i, z_i). This represents the position
            at which the optical mode is calculated.
        source_optical_mode: Torch tensor representing the source optical
            mode (complex number representing amplitude and phase).
        wavelength: Wavelength of the light.

    Returns:
        Torch tensor representing the optical mode at the detector position.
        Keep in mind that the optical mode is complex-valued.
    """
    # find the radial distance r
    r = (source_position-detector_position)**2
    r = torch.sqrt(torch.sum(r))

    # split equation into multiple components, so it's easier to  multiply
    # j is the imaginary number
    j = torch.tensor([1.j])

    # factor term
    factor = (source_position[2]-detector_position[2])/r**2

    # inverse radius term
    inverse_distance = 1/(2*math.pi*r)

    # inverse wavelength
    inverse_wavelength = 1/(j*wavelength)

    # exponential term
    exponential_term = torch.exp(j*2*math.pi*r/wavelength)

    # calculate the optical mode and return it
    w = factor*(inverse_distance+inverse_wavelength)*exponential_term
    return w*source_optical_mode


def generate_find_optical_mode_function(detector_position: torch.tensor,
                                        wavelength: float) -> Callable:
    """ Generates a find_optical_mode callable function from a given
    detector position and wavelength.

    Args:
        detector_position: Torch tensor representing the coordinates of the
            of detector (x_i, y_i, z_i). This represents the position
            at which the optical mode is calculated.
        wavelength: Wavelength of the light.

    Returns:
        Callable function of type find_optical_mode but with given
        detector position and wavelength.
    """
    # create the function
    def find_optical_mode_given_location(x: torch.tensor) -> torch.tensor:
        return find_optical_mode(
            source_position=x,
            detector_position=detector_position,
            wavelength=wavelength
        )

    # return the callable function
    return find_optical_mode_given_location


def find_optical_mode_from_source_array(
                                    source_matrix_position: torch.tensor,
                                    detector_position: torch.tensor,
                                    source_matrix_optical_mode: torch.tensor,
                                    wavelength: float) -> torch.tensor:
    """ Finds the optical mode from a given matrix of sources at a given
    detector position.

    Args:
        source_matrix_position: Tensor representing the position of all
            sources (n_source, n_source, 3) where the last entry is (x, y, z)
        detector_position: Torch tensor representing the coordinates of the
            of detector (x_i, y_i, z_i). This represents the position
            at which the optical mode is calculated.
        source_matrix_optical_mode: Torch tensor representing the optical modes
            of all sources from the array.
        wavelength: Wavelength of the light.

    Returns:
        Torch tensor representing the optical mode at the detector position.
        Keep in mind that the optical mode is complex-valued.
    """
    # the optical mode given from the sum off all sources
    total_optical_mode = torch.tensor([0+0j])

    # find the optical mode for each source in the matrix
    for i in range(source_matrix_position.shape[0]):
        for j in range(source_matrix_position.shape[1]):
            optical_mode = find_optical_mode(
                source_position=source_matrix_position[i][j],
                detector_position=detector_position,
                source_optical_mode=source_matrix_optical_mode[i][j],
                wavelength=wavelength
            )
            # add the optical mode to the total optical mode
            total_optical_mode = torch.add(
                total_optical_mode, optical_mode
            )

    # return the total optical mode
    return total_optical_mode


def find_optical_modes(source_matrix_position: torch.tensor,
                       detector_matrix_position: torch.tensor,
                       source_matrix_optical_mode: torch.tensor,
                       wavelength: float) -> torch.tensor:
    """ Finds the optical modes from a given matrix of sources at a given
    matrix of detector positions.

    Args:
        source_matrix_position: Tensor representing the position of all
            sources (n_source, n_source, 3) where the last entry is (x, y, z)
        detector_matrix_position: Tensor representing the position of all
            sources (n_detector, n_detector, 3) where the last entry is
            (x_i, y_i, z_i). This represents the position at which the optical
            modes are  calculated.
        source_matrix_optical_mode: Torch tensor representing the optical modes
            of all sources from the array.
        wavelength: Wavelength of the light.

    Returns:
        Torch tensor representing the optical mode at the detector position.
        Keep in mind that the optical mode is complex-valued.
    """
    # generate a tensor of the same shape as detector_matrix_position
    # but only one entry (complex-valued) for the optical modes
    optical_modes = torch.zeros(size=(detector_matrix_position.shape[0],
                                      detector_matrix_position.shape[1]),
                                dtype=torch.cfloat
                                )
    # go through each element and find it's corresponding optical mode
    for i in range(detector_matrix_position.shape[0]):
        for j in range(detector_matrix_position.shape[1]):
            # optical mode at a given detector point
            optical_mode = find_optical_mode_from_source_array(
                source_matrix_position=source_matrix_position,
                detector_position=detector_matrix_position[i][j],
                source_matrix_optical_mode=source_matrix_optical_mode,
                wavelength=wavelength
            )
            # give the value of optical mode tp each entry in the optical modes
            # tensor
            optical_modes[i][j] = optical_mode

    # return the optical modes
    return optical_modes


def find_intensity_map(optical_modes: torch.tensor) -> torch.tensor:
    """ Finds the normalized light intensities from a given optical mode map.

    Args:
        optical_modes: Torch tensor representing the matrix of optical
            modes.

    Returns:
        Torch tensor representing the light intensity of optical modes.
    """
    # maximum value of the optical modes value
    max_value = torch.max(torch.abs(optical_modes))

    # intensity map
    intensity_map = torch.abs(optical_modes)
    intensity_map = (torch.divide(intensity_map, max_value))**2

    # return the intensity map
    return intensity_map


if __name__ == '__main__':
    from utils import find_coordinate_matrix
    from matplotlib import pyplot as plt
    import numpy as np

    # used only for testing and debugging
    # create a coordinate matrix for a 28x28 source array placed at z=0
    debug_source_matrix = find_coordinate_matrix(n_size=10, n_length=1,
                                                 z_coordinate=0)

    # create a coordinate matrix for a 28x28 detector array placed at z=1
    debug_detector_matrix = find_coordinate_matrix(n_size=10, n_length=1,
                                                   z_coordinate=1)

    # use torch tensor
    debug_source_matrix = torch.from_numpy(debug_source_matrix)
    debug_detector_matrix = torch.from_numpy(debug_detector_matrix)

    # create a coherent optical mode map for sources and make the letter 5
    debug_source_mode = np.zeros(shape=(10, 10))
    debug_source_mode[8][2:8] = 1.0
    debug_source_mode[5][2:8] = 1.0
    debug_source_mode[2][2:8] = 1.0
    debug_source_mode[4][7] = 1.0
    debug_source_mode[3][7] = 1.0
    debug_source_mode[6][2] = 1.0
    debug_source_mode[7][2] = 1.0
    debug_source_mode = np.ones(shape=(10, 10))
    plt.title('Input Source of constant phase and amplitude')
    plt.imshow(debug_source_mode, origin='lower')
    plt.colorbar()
    plt.show()

    # create a torch tensor from numpy
    debug_source_mode = torch.from_numpy(debug_source_mode)

    # find the optical modes at the detector matrix
    debug_optical_modes = find_optical_modes(
        source_matrix_position=debug_source_matrix,
        detector_matrix_position=debug_detector_matrix,
        source_matrix_optical_mode=debug_source_mode,
        wavelength=652E-9
    )

    # find light intensity at the detector
    debug_light_intensity = find_intensity_map(
        optical_modes=debug_optical_modes)

    # plot the light intensity
    plt.title('Detector measurement at a distance of 1 meter')
    debug_light_intensity = debug_light_intensity.detach().cpu().numpy()
    plt.imshow(debug_light_intensity, origin='lower')
    plt.colorbar()
    plt.show()

