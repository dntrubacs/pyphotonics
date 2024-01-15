import numpy as np
from matplotlib import pyplot as plt
from diffractive_layers import InputLayer, DiffractiveLayer, DetectorLayer
import torch

# load data as numpy and transofrms to torch tensors
train_data = torch.from_numpy(np.load('test_data', allow_pickle=True))
train_labels = torch.from_numpy(np.load('test_labels', allow_pickle=True))
test_data = torch.from_numpy(np.load('test_data', allow_pickle=True))
test_labels = torch.from_numpy(np.load('test_labels', allow_pickle=True))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

train_data = train_data.type(torch.DoubleTensor).to(device)/255.0
train_labels = train_labels.type(torch.DoubleTensor).to(device)

# create torch model that can train on the data
class DiffractiveNN(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.wavelength = 0.652
        self.neuron_size = 10
        self.input = InputLayer(size=28, length=self.length, z_coordinate=0.0,
                                z_next=0.1,
                                size_next=self.neuron_size,
                                wavelength=self.wavelength)
        self.diffractive_layer_1 = DiffractiveLayer(size=self.neuron_size,
                                                    length=self.length,
                                                    z_coordinate=0.2,
                                                    z_next=0.3,
                                                    wavelength=self.wavelength)
        self.diffractive_layer_2 = DiffractiveLayer(size=self.neuron_size,
                                                    length=self.length,
                                                    z_coordinate=0.3,
                                                    z_next=0.4,
                                                    wavelength=self.wavelength)
        self.diffractive_layer_3 = DiffractiveLayer(size=self.neuron_size,
                                                    length=self.length,
                                                    z_coordinate=0.4,
                                                    z_next=0.5,
                                                    wavelength=self.wavelength)
        self.diffractive_layer_4 = DiffractiveLayer(size=self.neuron_size,
                                                    length=self.length,
                                                    z_coordinate=0.5,
                                                    z_next=0.6,
                                                    wavelength=self.wavelength)
        self.diffractive_layer_5 = DiffractiveLayer(size=self.neuron_size,
                                                    length=self.length,
                                                    z_coordinate=0.6,
                                                    z_next=0.7,
                                                    wavelength=self.wavelength)
        self.detector_layer = DetectorLayer(size=10, length=self.length,
                                            z_coordinate=0.7)

    def forward(self, x):
        x = self.input(x)
        x = self.diffractive_layer_1(x)
        x = self.diffractive_layer_2(x)
        x = self.detector_layer(x)
        return x


# build the model
model = DiffractiveNN().to(device)

# loss and optimizer
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.00001)

n_epochs = 10
for epoch in range(n_epochs):
    for i in range(train_data.shape[0]):
        output = model(train_data[i])
        loss = criterion(output, train_labels[i])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # copy the output and show it as plt
        if i % 2000 == 0:
            print('epoch:', epoch, 'i: ', i, ' loss: ', loss)
            np_output = output
            np_output = np_output.detach().cpu().numpy()
            plot_label = train_labels[i].detach().cpu().numpy()
            plot_data = train_data[i].detach().cpu().numpy()
            plt.figure()
            plt.title(f'Image {i}')
            plt.imshow(plot_data)
            plt.colorbar()
            plt.show()

            plt.figure(figsize=(8, 4))
            plt.subplot(121, title=f'Prediction after epoch: {epoch}')
            plt.imshow(np_output, origin='lower')
            plt.colorbar()
            plt.subplot(122, title=f'Label')
            plt.imshow(plot_label, origin='lower')
            plt.colorbar()
            plt.show()


# save the trained model
torch.save(model.state_dict(), 'trained_model/model_0')







