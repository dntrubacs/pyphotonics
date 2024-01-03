"""
Created by Daniel-Iosif Trubacs on 2 January 2024 for the UoS Integrated
Nanophotonics Group. The purpose of this module is to create a diffractive
layer class (based on the PyTorch architecture) DiffractiveLayer to be used on
the simulation of optical neural networks.

For more information about the mathematical algorithms behind the optical
neural network used please check the following References:

1. https://www.science.org/doi/10.1126/science.aat8084#supplementary-materials
"""
import numpy as np
import torch
from utils import find_coordinate_matrix
from matplotlib import pyplot as plt


class DiffractiveLayer(torch.nn.Module):
    """ Diffractive Layer based on the Lin2018 paper built using the
    PyTorch backend.

    The diffractive layer's weights represent a matrix with complex valued
    elements that have an amplitude (always between 0 and 1) and phase (always
    between 0 and 2*pi). The forward pass is based on the Rayleigh-Sommerfeld
    diffraction equation (see Reference 1). As the amplitude part of the
    transmission can only be between 0 and 1, the weights are always clipped
    to have an absolute value smaller than 1.

    Attributes:
        size: The numbers of neurons in a given collumn or row (the total
            number of neurons will be n_size x n_size). The values of the
            neurons is complex, and it will always have the form:
            a*e^(j*phase).
        length: The length of the matrix (corresponding to a physical
            implementation of the layer). This is used to find the coordinates
            of each neuron.
        neuron_length: The length of one physical neuron (length/size).
        weights: torch.nn.Parameter object containing a size x size
            matrix with the complex valued weights.
        z_coordinate: The z coordinated of the layer implemented (corresponding
            to the physical implementation). Keep in mind that all neurons will
            have this z coordinates as their position.
        neuron_coordinates: Tensor of shape (size, size, 3) representing the
            position of all neurons (x, y, z). See utils.find_coordinate_matrix
            for more information.
    """

    def __init__(self, size: int, length: float, z_coordinate: float) -> None:
        super().__init__()
        self.size = size
        self.length = length
        self.neuron_length = self.length / self.size
        self.z_coordinate = z_coordinate

        # initialize a size x size matrix and instantiate all elements as
        # Parameters
        self.weights = torch.nn.Parameter(torch.randn(size=(size, size),
                                                      dtype=torch.cfloat))

        # the position of each neuron
        self.neuron_coordinates = torch.from_numpy(find_coordinate_matrix(
            n_size=self.size, n_length=self.length,
            z_coordinate=self.z_coordinate
        ))

    def _clip_weights(self) -> torch.tensor:
        # always clip the weights to have an absolute values smaller than 1
        # keep only the absolute values who are greater than 1
        new_amplitude_weights = torch.clamp(torch.abs(self.weights), min=1)

        # divide the tensors element wise to get rid of all the weights with
        # amplitude larger than
        new_amplitude_weights = torch.div(self.weights, new_amplitude_weights)

        # return the new amplitude weights
        return new_amplitude_weights

    def _get_amplitude_map(self) -> np.ndarray:
        """ Gets the amplitude map of the neurons weights.

        Returns:
            Numpy arrays of shape (size, size) containing the
            absolute value of each weight.
        """
        # always clip the weights before plotting them
        clipped_weights = self._clip_weights()

        # copy the weights to a numpy array
        numpy_weights = clipped_weights.detach().cpu().numpy()

        return np.absolute(numpy_weights)

    def _get_phase_map(self) -> np.ndarray:
        """ Gets the phase map of the neurons weights.

        Returns:
            Numpy arrays of shape (size, size) containing the phase
            value of each weight.
        """
        # copy the weights to a numpy array
        numpy_weights = self.weights.detach().cpu().numpy()

        return np.angle(numpy_weights)

    def plot_amplitude_map(self) -> None:
        """Plots the amplitude map."""
        # if the number of neurons is greater than 15, the labels get
        # too crowded, so show only 15 values.
        if self.size < 15:
            x_ticks = ((np.arange(start=0, stop=self.size) + 0.5) *
                       self.neuron_length)
            y_ticks = ((np.arange(start=0, stop=self.size) + 0.5) *
                       self.neuron_length)

        else:
            x_ticks = (np.linspace(start=0,
                                   stop=self.size,
                                   num=15) + 0.5) * self.neuron_length
            y_ticks = (np.linspace(start=0,
                                   stop=self.size,
                                   num=15) + 0.5) * self.neuron_length

        # show the figure
        plt.figure(figsize=(12, 8))
        plt.title('Amplitude Map')
        plt.xlabel('x-position (m)')
        plt.ylabel('y-position (m)')
        plt.xticks(x_ticks)
        plt.yticks(y_ticks)
        plt.imshow(
            X=self._get_amplitude_map(),
            origin='lower',
            extent=[0, self.length, 0, self.length]
        )
        plt.colorbar()
        plt.show()

    def plot_phase_map(self) -> None:
        """Plots the phase map."""
        # if the number of neurons is greater than 15, the labels get
        # too crowded, so show only 15 values.
        if self.size < 15:
            x_ticks = ((np.arange(start=0, stop=self.size) + 0.5) *
                       self.neuron_length)
            y_ticks = ((np.arange(start=0, stop=self.size) + 0.5) *
                       self.neuron_length)

        else:
            x_ticks = (np.linspace(start=0,
                                   stop=self.size,
                                   num=15) + 0.5) * self.neuron_length
            y_ticks = (np.linspace(start=0,
                                   stop=self.size,
                                   num=15) + 0.5) * self.neuron_length

        # show the figure
        plt.figure(figsize=(12, 8))
        plt.title('Phase Map (measured in radians)')
        plt.xlabel('x-position (m)')
        plt.ylabel('y-position (m)')
        plt.xticks(x_ticks)
        plt.yticks(y_ticks)
        plt.imshow(
            X=self._get_phase_map(),
            origin='lower',
            extent=[0, self.length, 0, self.length]
        )
        plt.colorbar()
        plt.show()

    def forward(self, x) -> torch.Tensor:
        """ Forward model based on the Rayleigh-Sommerfeld model. Please
        check the reference supllemnetary for more details.

        Args:
            x: Tensor representing the values of the output of the layer before
                at the given points where the wights are (has to be the same
                size as the weights).

        Returns:
            Tensor representing the output of this layer at the given points
            of the next layer.
        """
        # the transmisison matrix containing the weights
        transmission_matrix = self._clip_weights()

        return transmission_matrix




if __name__ == '__main__':
    # used only for testing and debugging
    debug_layer = DiffractiveLayer(size=200, length=10, z_coordinate=0)
    debug_layer.forward(x=2)