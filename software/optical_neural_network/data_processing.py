from data_processing_utils import create_detector_from_label
import idx2numpy
import numpy as np
from matplotlib import pyplot as plt
import pickle

data_file = 't10k-images.idx3-ubyte'
label_file = 't10k-labels.idx1-ubyte'
data = idx2numpy.convert_from_file(data_file)
labels = idx2numpy.convert_from_file(label_file)

detector_labels = np.zeros(shape=(data.shape[0], 10, 10))
for i in range(detector_labels.shape[0]):
    detector_labels[i] = create_detector_from_label(labels[i])


with open('test_data', 'wb') as handle:
    pickle.dump(data, handle)

with open('test_labels', 'wb') as handle:
    pickle.dump(detector_labels, handle)
