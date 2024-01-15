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

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def find_optical_modes(source_positions: torch.Tensor,
                           detector_positions: torch.Tensor,
                           source_optical_modes: torch.Tensor,
                           wavelength: torch.cfloat) -> torch.Tensor:
    """Finds the optical modes at multiple positions from multiple sources.

    Args:
        source_positions: Torch tensor representing the coordinates of the
            sources (x, y, z) having shape (M, N, 3).
        detector_positions: Torch tensor representing the coordinates of the
            detectors (x_i, y_i, z_i) for each source, having shape (K, L, 3).
        source_optical_modes: Torch tensor representing the source optical
            modes (complex number representing amplitude and phase) for each
            source, having shape (M, N).
        wavelength: Wavelength of the light.

    Returns:
        Torch tensor representing the optical modes at the detector positions.
        The optical mode is complex-valued and the returned shape is (N, M).
    """
    # complex unit 'j'
    complex_i = torch.tensor(1.j, dtype=torch.cfloat, device=device)

    # Broadcast detector positions to have the same shape as source positions
    # detector array of shape (K,L)
    # source array of shape (M,N)
    pos_src_broadcast = source_positions.unsqueeze(0).unsqueeze(
        0).to(device)  # shape will be (1, 1, M, N, 3)
    pos_det_broadcast = detector_positions.unsqueeze(2).unsqueeze(
        2).to(device)  # shape will be (K, L, 1, 1, 3)
    modes_src_broadcast = source_optical_modes.unsqueeze(0).unsqueeze(
        0).to(device)  # shape will be (1, 1, M, N, 3)

    # Calculate the radial distance r for each source-detector pair
    squared_diff = (pos_src_broadcast - pos_det_broadcast) ** 2
    r = torch.sqrt(torch.sum(squared_diff,
                             dim=-1))  # sum along the last dimension (x, y, z)

    # z-distance, z/r^2 factor, inverse distance, and inverse wavelength
    z_diff = pos_src_broadcast[..., 2] - pos_det_broadcast[..., 2]
    zr2_factor = z_diff / r ** 2
    inverse_distance = 1 / (2 * torch.pi * r)
    inverse_wavelength = 1 / (complex_i * wavelength)

    # phase term
    exponential_term = torch.exp(complex_i * 2 * torch.pi * r / wavelength)

    # contribution from all sources for each detector
    w = zr2_factor * (inverse_distance + inverse_wavelength) * exponential_term
    w_s = w * modes_src_broadcast

    # `w_s` is now a large array of shape (K, L, M, N), containing the complex
    # amplitude of every (MxN) source's contribution to every (KxL) detector

    # superpose fields: for each detector, sum over source positions the total, local, complex amplitude
    total_A = w_s.sum(dim=(2, 3))  # dimensions 0 and 1 are detector pos.

    return total_A

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
    debug_source_matrix = find_coordinate_matrix(n_size=40, n_length=1,
                                                 z_coordinate=0)

    # create a coordinate matrix for a 28x28 detector array placed at z=1
    debug_detector_matrix = find_coordinate_matrix(n_size=40, n_length=1,
                                                   z_coordinate=1)

    # use torch tensor
    debug_source_matrix = torch.from_numpy(debug_source_matrix)
    debug_detector_matrix = torch.from_numpy(debug_detector_matrix)

    # create a coherent optical mode map for sources and make the letter 5
    debug_source_mode = np.ones(shape=(40, 40))
    plt.title('Input Source of constant phase and amplitude')
    plt.imshow(debug_source_mode, origin='lower')
    plt.colorbar()
    plt.show()

    # create a torch tensor from numpy
    debug_source_mode = torch.from_numpy(debug_source_mode)

    # find the optical modes at the detector matrix
    debug_optical_modes = find_optical_modes(
        source_positions=debug_source_matrix,
        detector_positions=debug_detector_matrix,
        source_optical_modes=debug_source_mode,
        wavelength=0.652
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

