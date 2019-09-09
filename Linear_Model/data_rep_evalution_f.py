# -*- coding: utf-8 -*-
"""Assignment_data_rep_evalution_f.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E_dUnhz5GCHQMa_jYcQDKhaX-aXkLveY

### Generate Random array
Generate a numpy array of shape x with random values as its elements.
"""

import numpy as np

def generate_array(x):
  '''
  input:
    x: tuple defining shape; Eg., (5, 2, 3)
  output:
    y: numpy array of shape x generated using numpy.random library
        and its elements as random values between [0,1).
  '''
  # YOUR CODE HERE
  y= np.random.random(x)
  return y

'''test for generate_array'''
def test_generate_array():
  x = (2,4,5,6)
  y = generate_array(x)
  assert y.shape==x
  assert np.all(y<1)
  assert np.all(y>=0)
  print('Test passed', '\U0001F44D')
test_generate_array()

"""### Shape
Write a python function to calculate shape of a given array.
"""

def return_shape(x):
  '''
  input:
    x: a numpy array of any dimension
  output:
    y: shape of input array as a tuple.
  '''
  # YOUR CODE HERE
  return x.shape

'''test for return_shape'''
def test_return_shape():
  x = np.array([1,2])
  y = return_shape(x)
  assert y == (2,)
  print('Test passed', '\U0001F44D')
test_return_shape()

"""### Mean and STD
Given a data tensor X,  with axis=0 indexing the samples, find mean and standard deviation of the samples .
"""

def CalculateMeanStddev(x):
  '''
  input:
    x: a numpy array of any dimension
  output:
    mean: Numpy array with mean of input samples
    stddev: Numpy array with standard deviation of input samples
  
  HINT: Shape of Input is (samples, feature1, feature2, ...)
  
  Return mean,stddev
  '''
  # YOUR CODE HERE
  mean=np.mean(x,axis=0)
  sd=np.std(x,axis=0)
  return mean,sd

'''test for CalculateMeanStddev'''
def test_CalculateMeanStddev():
  X = np.array([[1,2,3],
                [5,3,1],
                [3,7,9],
                [3,5,6]])
  mean, stddev = CalculateMeanStddev(X)
  assert np.all(np.isclose(mean, np.array([3.  , 4.25, 4.75])))
  assert np.all(np.isclose(stddev, np.array([1.41421356, 1.92028644, 3.03108891]) ))

  print('Test passed', '\U0001F44D')
test_CalculateMeanStddev()

"""### Index
Given a matrix of size (m,n) find the element at index position i = a, j =b (start indexing from 0)
(Note: If m<a+1 or n<b+1, then return 'None')
"""

def element_at_given_index_position(x,a,b):
  '''
  input:
    x: numpy array of shape (m,n)
    a: integer value (row)
    b: integer value (column)
  output:
    y: element at index position (a,b)
  '''
  # YOUR CODE HERE
  m=x.shape[0]
  n=x.shape[1]
  for i in range(0,m):
    for j in range(0,n):
      return x[a,b]
    
  if (m<a+1):
    return "None"
  elif (n<b+1):
    return "None"

'''test for  element_at_given_index_position'''
def test_element_at_given_index_position():
  
  
  x = np.array([[1,2,3],
                [5,3,1],
                [3,7,9],
                [3,5,6],
                [1,2,3],
                [5,7,8]])
  z =  element_at_given_index_position(x,5,2)
  assert z ==8
  print('Test passed', '\U0001F44D')
  
test_element_at_given_index_position()

"""### Batch splitting
Given a data matrix X with axis = 0 for samples, split X into batches of 'm' samples each.
Note: last batch can have  less than 'm' samples.
Output should be list of numpy arrays.
"""

def split_data(x,m):
  '''
  input:
    x: 2d numpy array of any shape (with axis = 0 indicating samples)
    m: integer (sample size iin each batch)
  output:
    y: a list containing numpy arrays with 'm' samples in each array and 
    can be less than m only in last array
  '''
  # YOUR CODE HERE
  Xbatches=[]
  Nb=int(np.ceil(x.shape[0]/m))
  for b in range(Nb):
    batch=x[b*m:(b+1)*m,:]
    Xbatches.append(batch)
  
  return Xbatches

'''test for  element_at_given_index_position'''
def test_split_data():
  
  
  x = np.array([[1,2,3],
                [5,3,1],
                [3,7,9],
                [3,5,6],
                [11,12,13],
                [5,7,8],
                [1,2,3],
                [5,3,1],
                [3,7,9],
                [3,5,6],
                [11,12,13],
                [5,7,8]])
  z = split_data(x,5)
  assert np.all(z[0]==np.array([[ 1,  2,  3],
       [ 5,  3,  1],
       [ 3,  7,  9],
       [ 3,  5,  6],
       [11, 12, 13]]))
  
  assert np.all(z[1]==np.array([[5, 7, 8],
       [1, 2, 3],
       [5, 3, 1],
       [3, 7, 9],
       [3, 5, 6]]))
  
  assert np.all(z[2]==np.array([[11, 12, 13],
       [ 5,  7,  8]]))

  print('Test passed', '\U0001F44D')
  
test_split_data()

"""### Shuffle
Given a data tensor X with axis = 0 indexing the sample, randomly shuffle the samples.
"""

def shuffle_samples(x):
  '''
  input:
    x: any general numpy array of dimension (m,n)
  output:
    y: a numpy array with dimension same as of input array but 
    samples are shuffled randomly.
  '''
  # YOUR CODE HERE
  np.random.shuffle(x)
  return x

def test_shuffle_samples():
  x = np.array([[1,2,3],
                [5,3,1],[6,8,0]])
  shuffle_samples(x)
  assert x.shape == (3,3)
  print('Test passed', '\U0001F44D')
  
test_shuffle_samples()

"""### 1-hot encoding
Given three classes, encode them as one hot encoded vectors. For example, if
y = [0, 1, 2] then one hot encoded y = [ [1, 0, 0] , [0, 1, 0] , [0, 0, 1] ]
"""

def oneHot(y, Ny):
  import numpy as np
  
  '''
  Input:
      y: an int in {0, 1, 2}
      Ny: Number of classes, e.g., 3 here.
  Output:
      Y: a vector of Ny (=3) tuples
    '''
  # YOUR CODE HERE
  Y=np.zeros(Ny)
  Y[y]=1
  return Y

def test_oneHot():
    assert np.all(oneHot(0,3)==np.array([1,0,0]))
    assert np.all(oneHot(1,3)==np.array([0,1,0]))
    assert np.all(oneHot(2,3)==np.array([0,0,1]))
   # assert Y_train.shape[1]==3
    print("Test passed', '\U0001F44D")
test_oneHot()

"""Given desired output in a list, convert output into one hot encoded vectors."""

def one_hot_encoding_output(x):
  '''
  input:
    x: a list containing desired output, for exmple x = ['cat', 'dog', 'mouse']
  output:
    y: numpy array with one hot encoded vectors as its elements.
  '''
  # YOUR CODE HERE
  #Make a list of unique elements called categories
  #categories=list(set(x))
  categories=[]
  for i in x:
    if i not in categories:
      categories.append(i)
    else:
      pass
  
  x_ind=[]
  for element in x:
    index = categories.index(element)
    x_ind.append(index)
   
  #for each element in x_ind, find the 1 hot encoded form
  
  x_1hot=[]
  for index in x_ind:
    onehotvec=oneHot(index, len(categories))
    x_1hot.append(onehotvec)
    
  return x_1hot

def test_one_hot_encoding_output():
    x = ['cat', 'dog', 'mouse']
    one_hot_encoding_output(x)[0]
    assert np.all(one_hot_encoding_output(x)[2]==np.array([0., 0., 1.]))
    assert np.all(one_hot_encoding_output(x)[1]==np.array([0., 1., 0.]))
    assert np.all(one_hot_encoding_output(x)[0]==np.array([1., 0., 0.]))
    print("Test passed', '\U0001F44D")
test_one_hot_encoding_output()

"""Given a data tensor X, with axis = 0 indexing the samples, randomly pick 10 samples and return as a numpy tensor.
If there are less than 10 samples, pad the output tensor with samples having all values as zero(hint. - padded samples will have same dimension as of input samples)
"""

def pick_samples(x):
  '''
  input:
    x: a numpy array of shape (m,n) (Note: it may have less than 10 samples also. Your code should be fit for 
    both conditions i.e. m<10 or m>10 )
  output:
    y: numpy array containing 10 samples selected by randomly shuffling input array and padding samples with all 
    elements as zeros if input array has less than 10 samples.
    .
  '''
  # YOUR CODE HERE
  m=x.shape[0]
  zero_array=[]
  newx=[]
  index=(10-m,x.shape[1])
  if(m>=10):
    rand_indices=np.random.randint(0,m,size=10)
    newx=x[rand_indices]
    return newx
  else:
    rand_indices=np.random.randint(0,m,size=m)
    newx=x[rand_indices]
    zero_array=np.zeros(index)
    return np.concatenate((newx,zero_array),axis=0)

def test_pick_sample():
    x = np.array([[1,2,3],
                 [5,3,1],
                 [3,7,9]])
    z = pick_samples(x)
    assert z.shape==(10,x.shape[1])
    print("Test passed', '\U0001F44D")
test_pick_sample()

def test_pick_sample():
   
  x = np.array([[1,2,3],
                [5,3,1]])
  Z = np.array
  assert np.all(one_hot_encoding_output(x)[2]==np.array([0., 0., 1.]))
  assert np.all(one_hot_encoding_output(x)[1]==np.array([0., 1., 0.]))
  assert np.all(one_hot_encoding_output(x)[0]==np.array([1., 0., 0.]))
  print("Test passed', '\U0001F44D")
test_one_hot_encoding_output()

"""### Confusion Matrix
Given the true output values of a classification task is a numpy vector Ytrue
and the estimated output values is  a numpy vector Yest , your function should return
the confusion matrix. Do not use any standard library.
"""

def draw_confusion_matrix(yest,ytrue):
  '''
  input:
    yest: one dimensional numy array consisting of predicted output values(for example  yest = [ 1, 0, 0, 1, 0, 0, 1, 1, 1, 0 ] )
    ytrue: one dimensional numy array consisting of actual output values)( for example, ytrue = [ 1, 1, 0, 1, 0, 0, 1, 0, 0, 0 ] )
  output:
    y: confusion matrix as a numpy array 
    .
  '''
  # YOUR CODE HERE
  m=len(yest)
  TP=0
  FN=0
  FP=0
  TN=0
  for i in range(0,m):
    if yest[i]==1:
      if ytrue[i]==1:
        TP=TP+1
      else:
        FP=FP+1
    else:
      if ytrue[i]==1:
        FN=FN+1
      else:
        TN=TN+1
  
  CM=[[TN,FN],
      [FP,TP]]
  return CM

yest = [ 1, 0, 0, 1, 0, 0, 1, 1, 1, 0 ]
ytrue = [ 1, 1, 0, 1, 0, 0, 1, 0, 0, 0 ]
draw_confusion_matrix(yest,ytrue)

from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
import numpy as np


expected = [ 1, 0, 0, 1, 0, 0, 1, 1, 1, 0 ]
predicted = [ 1, 1, 0, 1, 0, 0, 1, 0, 0, 0 ]
results = confusion_matrix(expected, predicted)
print(results)

''' check for draw confusion matrix'''

from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
import numpy as np


expected = [ 1, 0, 0, 1, 0, 0, 1, 1, 1, 0 ]
predicted = [ 1, 1, 0, 1, 0, 0, 1, 0, 0, 0 ]
results = confusion_matrix(expected, predicted)
assert np.all(draw_confusion_matrix(expected,predicted) == results)
print("Test passed', '\U0001F44D")

"""Given the confusion matrix CM = np.array([[40 20 10],
                                                                          [10 30 5],
                                                                          [2 1 50]])
 

1.   What is the accuracy? Save it as 'acc.'.
2.   What is precision? Save it as 'prec' in a numpy array.
3.   What is recall? Save it as 'recall' in a numpy array
4.   What is F-1 score? Save it as 'F_1' in a numpy array
"""

def confusion_matrix_metrics(CM):
  '''
    input:
      CM: confusion matrix
    output:
      accuracy: Accuracy across all classes
      precision: Numpy array with precision for each class
      recall: Numpy array with recall for each class
      F_1 : Numpy array with f_1 score for each class
      
      Return the results as a tuple (accuracy, precision, recall, f_1)
  '''
  sum_true=0
  for i in range (CM.shape[0]):
    sum_true=sum_true+CM[i][i]
  accuracy=sum_true/CM.sum()
  
  lprec=[]
  lrec=[]
  
  for i in range (CM.shape[0]):
    sum_prec=np.sum(CM,axis=0)[i]
    lprec.append(CM[i,i]/sum_prec)
  precision=np.array(lprec)
  
  for i in range(CM.shape[1]):
    sum_recall=np.sum(CM,axis=1)[i]
    lrec.append(CM[i,i]/sum_recall)
  recall=np.array(lrec)
  
  F_1=((2*precision*recall)/(precision+recall))
  
  return tuple([accuracy,precision,recall, F_1])

''' check for confusion matrix'''

def test_confusion_matrix_metrics():
  CM = np.array([[40,20,10], [10,30,5], [2,1,50]])
  accuracy, precision, recall, F_1 = confusion_matrix_metrics(CM) 
  
  assert np.isclose(accuracy, 0.7142857142857143)
  assert np.all(np.isclose(precision, np.array([0.7692307692307693, 0.5882352941176471, 0.7692307692307693])))
  assert np.all(np.isclose(recall, np.array([0.5714285714285714, 0.6666666666666666, 0.9433962264150944])))
  assert np.all(np.isclose(F_1, np.array([0.6557377049180327, 0.625, 0.847457627118644])))
  print("Test passed', '\U0001F44D")
  
test_confusion_matrix_metrics()

