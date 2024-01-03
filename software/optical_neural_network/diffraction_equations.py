"""
Created by Daniel-Iosif Trubacs on 3 January 2024 for the UoS Integrated
Nanophotonics Group. The purpose of this module is to create certain
diffraction equations based on the Rayleigh-Sommerfeld model. The equation
for the optical w at a position (x,y,z) generated from a source at position
(x_i, z_i, z_i) and wavelength lambda is:
w = (z-z_i)/r**2 * (1/(2*pi*r) + 1/(lambda*j))*exp(j*2*pi*r/lambda) (1)
  = factor*(inverse_distance + inverse_wavelength)*exponential_term

where r = sqrt((x-x_i)**2 + (y-y_i)**2 + (z-z_i)**2) and j is the imaginary
number sqrt(-1).

All the calculations are done using the torch backend as this integrates easier
with neural network architecture.

For more information about the mathematical algorithms behind the optical
neural network used please check the following References:

1. https://www.science.org/doi/10.1126/science.aat8084#supplementary-materials
"""

import torch
import math


def find_optical_mode(source_position: torch.tensor,
                      detector_position: torch.tensor,
                      wavelength: float) -> torch.tensor:
    """ Finds the optical mode at a given position from a given source.

    The output function is based on the
    Args:
        source_position: Torch tensor representing the coordinates of the
            source (x, y, z).
        detector_position: Torch tensor representing the coordinates of the
            of detector (x_i, y_i, z_i). This represents the position
            at which the optical mode is calculated.
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
    return w


if __name__ == '__main__':
    # used only for testing and debugging
    debug_source_position = torch.tensor([1.0, 1.0, 1.0])
    debug_detector_position = torch.tensor([1.0, 1.0, 2.0])
    find_optical_mode(source_position=debug_source_position,
                      detector_position=debug_detector_position,
                      wavelength=652E-9)



