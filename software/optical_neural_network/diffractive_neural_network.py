import numpy as np
from matplotlib import pyplot as plt
from diffractive_layers import InputLayer, DiffractiveLayer, DetectorLayer
import torch

# load data as numpy and transofrms to torch tensors
train_data = torch.from_numpy(np.load('test_data', allow_pickle=True))
train_labels = torch.from_numpy(np.load('test_labels', allow_pickle=True))
test_data = torch.from_numpy(np.load('test_data', allow_pickle=True))
test_labels = torch.from_numpy(np.load('test_labels', allow_pickle=True))

train_data = train_data.type(torch.float32)
train_labels = train_labels.type(torch.float32)

# create torch model that can train on the data
class DiffractiveNN(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.wavelength = 652E-9
        self.neuron_size = 10
        self.input = InputLayer(size=28, length=self.length, z_coordinate=0.0,
                                z_next=self.neuron_size,
                                size_next=self.neuron_size,
                                wavelength=self.wavelength)
        self.diffractive_layer_1 = DiffractiveLayer(size=self.neuron_size,
                                                    length=self.length,
                                                    z_coordinate=0.2,
                                                    z_next=0.3,
                                                    wavelength=652E-9)
        self.diffractive_layer_2 = DiffractiveLayer(size=self.neuron_size,
                                                    length=self.length,
                                                    z_coordinate=0.3,
                                                    z_next=0.4,
                                                    wavelength=652E-9)
        self.detector_layer = DetectorLayer(size=10, length=10,
                                            z_coordinate=10)

    def forward(self, x):
        x = self.input(x)
        x = self.diffractive_layer_1(x)
        x = self.diffractive_layer_2(x)
        x = self.detector_layer(x)

        return x

# build the model
model = DiffractiveNN()

# loss and optimizer
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

n_epochs = 1

for epoch in range(n_epochs):
    for i in range(100):
        print(model.diffractive_layer_1.weights)
        print(model.diffractive_layer_2.weights)
        output = model(train_data[i])
        show = model.input.weights.detach().cpu().numpy()
        plt.imshow(show)
        plt.show()
        loss = criterion(output, train_labels[i])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print('i: ', i, ' loss: ', loss)

        # copy the output and show it as plt
        if i % 1 == 0:
            np_output = output
            np_output = np_output.detach().cpu().numpy()
            plt.title(f'Output after data: {i}')
            plt.imshow(np_output, origin='lower')
            plt.colorbar()
            plt.show()












