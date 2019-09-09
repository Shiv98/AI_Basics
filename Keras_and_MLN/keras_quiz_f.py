# -*- coding: utf-8 -*-
"""Copy of keras_quiz_f.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m76yiowNIuurIxkCGqq3xXTXXWYlYpj1

## Build a model using Keras
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

### Download data from google drive. You need not mess with this code.

import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                
if __name__ == "__main__":
    file_id = '1DHF4b0sBB_KLQ4oxNEMp0sGrViu0gpeG'
    destination = 'data.csv'
    download_file_from_google_drive(file_id, destination)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests


# Importing and cleaning data using pandas library
data = pd.read_csv('data.csv')

## Last column is output features. Rest are inputs
X = data.iloc[:, 1:-1].values

# 2nd column is output labels
y = data.iloc[:, -1].values

print(np.amax(y), np.amin(y))

"""Convert labels to intermediate representation where each label is replaced by a number from 0 to Ny-1
(Ny is number of classes)
"""

def conv_labels(y_raw):
    """
    Inputs:
        y_raw: numpy array of labels
    Outputs:
        y: numpy array of ints, each label is replaced by an int from 0 to Ny-1
        Ny: number of classes
    """
    # YOUR CODE HERE
    y =  []
    uniques = np.unique(y_raw).tolist()
    for i in y_raw:
      y.append(uniques.index(i))
    y = np.array(y)
    Ny = len(uniques)
    return y, Ny



### One-hot encode Y_v
def oneHot(y, Ny):
    '''
    Input:
        y: an int in {0, Ny -1 }
        Ny: Number of classes, e.g., 2 here.
    Output:
        Y: a vector of shape (Ny,)
    '''
    # YOUR CODE HERE
    Y = np.zeros(Ny)
    Y[y] = 1
    
    from keras.utils import to_categorical
    Y = to_categorical(y, Ny)
    return Y

"""Test for one-hot"""
assert np.all(oneHot(0,3)==np.array([1,0,0]))

"""#### Create Y_o which is one-hot encoding of Y using above functions"""

def create_Y_o(y):
    """
    Inputs:
        y: numpy array of class labels
    Outputs:
        Y_o: numpy array of shape(samples, Ny) with one-hot encodings of y
        Ny: number of unique classes
    """
    # YOUR CODE HERE
    y, Ny = conv_labels(y)
    Y_o = np.zeros((y.shape[0], Ny))
    for i in range(y.shape[0]):
      Y_o[i] = oneHot(y[i], Ny)
    return Y_o, Ny

Y_o, Ny = create_Y_o(y)



### Split data into train and test. Keep 10% of samples for testing
## Divide the data into these variables - X_train, X_test, y_train, y_test
# YOUR CODE HERE
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y_o, test_size = 0.1)

"""test for splitting"""
assert(X_train.shape[0] == 13608)

## Normalize the Data
def findMeanStddev(X):
    '''
    Input: 
        X: a matrix of size (no. of samples, dimension of each sample)
    Output:
        mean: mean of samples in X (same size as X)
        stddev: element-wise std dev of sample in X (same size as X)
    '''
    # YOUR CODE HERE
    mean = np.sum(X, axis = 0)/X.shape[0]
    stddev = np.std(X, axis = 0)
    return mean, stddev

sum = np.sum(X_train, axis = 0)
np.any(np.isnan(X_train/X_train.shape[0]))

def normalizeX(X, mean, stddev):
    '''
    Input:
        X: a matrix of size (no. of samples, dimension of each sample)
        mean: mean of samples in X (same size as X)
        stddev: element-wise std dev of sample in X (same size as X) 
    Output:
        Xn: X modified to have 0 mean and 1 std dev
    '''
    # YOUR CODE HERE
    Xn = (X - mean)/(stddev + 10**(-8))
    return Xn

mean_train, stddev_train = findMeanStddev(X_train)
X_train = normalizeX(X_train, mean_train, stddev_train)
X_test = normalizeX(X_test, mean_train, stddev_train)

np.any(np.isnan(X_train))

print(mean_train, stddev_train)
np.any(np.isnan(mean_train))

"""#### Create model. 
- Choose the number of hidden layers, neurons, activations, loss function, learning rate and optimizers on your own.
- Report accuracy metric
- Use no more than 100 epochs
- Use validation_split = 0.1
"""

print(X.shape[1:])

import keras
def create_model():
    """
    Inputs:
        None
    Outputs:
        model: keras model afteer compiling
    """
    # YOUR CODE HERE
    from keras.layers import Input, Dense
    from keras.models import Model
    
    input_layer = Input(shape = X_train.shape[1:])
    h1 = Dense(10, activation = 'sigmoid')(input_layer)
    output_layer = Dense(Ny, activation = 'softmax')(h1)
    
    model = Model(inputs = [input_layer], outputs=[output_layer])
    model.compile(loss='categorical_crossentropy', optimizer = 'sgd', metrics = ['accuracy'])
    return model



model = create_model()
history = model.fit(X_train, y_train, epochs=100, batch_size = 100, validation_split = 0.1)

from matplotlib import pyplot as plt
plt.plot(history.history['val_acc'])

"""#### Evalutaion

Test for model

Test for model

Test for model

#### Confusion Matrix
"""

def create_cm(Y_test, Y_pred):
    """
    Inputs:
        Y_test: numpy array with true labels
        Y_pred: numpy array with predicted labels
    Outputs:
        CM: numpy array (ndim=2) containing confusion matrix
    """
    # YOUR CODE HERE
    from sklearn.metrics import confusion_matrix
    CM= confusion_matrix(Y_test.argmax(axis=1), Y_pred.argmax(axis = 1))
    return CM




