# -*- coding: utf-8 -*-
"""word2vec_assignment_f.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13PajoRHAlXMRgphx263jG6S4awcJRogs

# (Word Embedding Training, Visualization, Evaluation)
Word Vectors are often used as a fundamental component for downstream NLP tasks, e.g. question answering, text generation, translation, etc., so it is important to build some intuitions as to their strengths and weaknesses.  <br>
**Note on Terminology:**
The terms "word vectors" and "word embeddings" are often used interchangeably. The term "embedding" refers to the fact that we are encoding aspects of a word's meaning in a lower dimensional space. As Wikipedia states, "conceptually it involves a mathematical embedding from a space with one dimension per word to a continuous vector space with a much lower dimension".

# Collect Data
The dataset  contains  10 sentences.
"""

import numpy as np

corpus = ['king is a strong man', 
          'queen is a wise woman', 
          'boy is a young man',
          'girl is a young woman',
          'prince is a young king',
          'princess is a young queen',
          'man is strong', 
          'woman is pretty',
          'prince is a boy will be king',
          'princess is a girl will be queen',
          'prince is a strong boy',
          'boy is strong',
          'girl is pretty',
          'girl will be woman',
          'boy will be man']

"""# Tokenization
For many NLP tasks, the first thing you need to do is to tokenize your raw text into lists of words. Suppose your have *text = "king is a strong man"*  You can just use *text.split("  ")* to break the sentences into a list of words. You will get output as "['king', 'is', 'a', 'strong', 'man']"
Write and run your code in the next cell to tokenize all the sentences. <br>
"""

def Tokenization(corpus):
    '''
    Input:
      corpus: list of sentences(Eg., The list 'corpus' contains 10 sentences as defined above)
    
    Output:
           y: list of lists, each sentence in corpus is broken into a list of words (obtained by tokenizing all the sentences)
    '''
    # YOUR CODE HERE
    y=[]
    for text in corpus:
      y.append(text.split(" "))
    return y

Tokenization(corpus)

'''test for Tokenization'''
def test_Tokenization():
  y = Tokenization(corpus)
  assert y[0]==['king', 'is', 'a', 'strong', 'man']
  assert y[9]==['princess', 'is', 'a', 'girl', 'will', 'be', 'queen']
  print('Test passed', '\U0001F44D')
test_Tokenization()

"""# Remove stop words
## Stopwords: 
Words such as articles and some verbs are usually considered stop words because they don’t help us to find the context or the true meaning of a sentence. These are words that can be removed without any negative consequences to the final model that you are training.
In order for efficiency of creating word vectors, we will remove commonly used words.<br>
For our case, lets take following list as stopwords. <br>
stop_words = ['is', 'a', 'will', 'be'] <br>
For example, ouput corrosponding to *"king is a strong man"* will be ['king', 'strong', 'man'] and your function should return list which don't have stop-words in it.<br>
"""

def remove_stop_words(corpus):
    '''
    Input:
      corpus: list of sentences(Eg., The list 'corpus' contains 10 sentences as defined above)
    
    Output:
      corpus_wo_stopwords: list of lists, each sentence in corpus is broken into a list of words excluding stop words 
                           (obtained after tokenizing the corpus followed by removing stop words)
    '''
    
    # Get stop-word list
    stop_words = ['is', 'a', 'will', 'be']
    
    # YOUR CODE HERE
    corpus_wo_stopwords=[]
    y=Tokenization(corpus)
    for i in y:
      temp=[]
      for j in i:
        if j not in stop_words:
           temp.append(j)
      corpus_wo_stopwords.append(temp)
    return corpus_wo_stopwords    
PP_corpus = remove_stop_words(corpus)

'''test for remove_stop_words'''
def test_remove_stop_words():
  assert set(PP_corpus[0])==set(['king', 'strong', 'man'])
  assert set(PP_corpus[9])==set(['princess', 'girl', 'queen'])
  print('Test passed', '\U0001F44D')
test_remove_stop_words()

"""# Create vocabulary
Building a vocabulary is nothing more than assigning a unique integer id to each word in the dataset. So, a vocabulary is basically a python dictionary data structure. The dictionary will map the word to a number. <br>
 E.g. dictionary['love'] = 520
Your function should return dictionary for unique words.<br>
For example, if you have three unique words, namely, *'princess', 'queen', 'girl',* then your output should be {'princess': 0, 'queen': 1, 'girl': 2}

### 1. Find out set of unique words in PP_corpus
"""

def get_unique_words(PP_corpus):
    '''
    Input:
        PP_corpus: list of lists containing the list of words (obtained after tokenizing the corpus followed by removing stop words)
    
    Output:
        unique_words: set of unique words in PP_corpus
    '''
    # YOUR CODE HERE
    u=[]
    for i in PP_corpus:
      for j in i:
        if j not in u:
          u.append(j)
    unique_words=set(u)
    
    return unique_words
  
unique_words = get_unique_words(PP_corpus)

unique_words

'''test for remove_stop_words'''
def test_unique_word():
  assert unique_words=={'strong', 'pretty', 'wise', 'queen', 'man', 'prince', 'king', 'young', 'princess', 'woman', 'boy', 'girl'}
  print('Test passed', '\U0001F44D')
test_unique_word()

"""### 2. Map the unique words to integers starting from 0"""

def mapping(unique_words):
    '''
    Input:
        unique_words: set of unique words in PP_corpus  
    Output:
        word2int: dictionary which maps the words in set unique_words to integers starting from 0 (of same length as unique_words)
    '''
    # YOUR CODE HERE
    word2int={}
    l=list(unique_words)
    print(l)
    i=0
    for j in l:
      word2int[j]=i
      i=i+1
    return word2int
    
word2int = mapping(unique_words)

word2int

'''test for mapping'''
def test_mapping():
  assert len(word2int)==12
  assert np.unique(list(word2int.values())).shape[0]==12
  print('Test passed', '\U0001F44D')
test_mapping()

"""## Prepare data for Skip-Gram Model 
In skip gram architecture of word2vec, the input is the center word and the predictions are the context words. Consider an array of words W, if W(i) is the input (center word), then W(i-2), W(i-1), W(i+1), and W(i+2) are the context words, for a sliding window size of 2.

![Sliding Window](https://cdncontribute.geeksforgeeks.org/wp-content/uploads/word2vec_diagram-1.jpg)

# data generation
The final structure of your data should be a list of tuples $(x, y)$.
$x$ is the id of the target word (the center word in current window) and $y$ is the id of the context word. This is well illustrated in above figure.
"""

import pandas as pd

def data_gen(PP_corpus, window_size):
    '''
    Input:
        PP_corpus: list of lists (obtained after tokenizing the corpus followed by removing stop words) 
        window_size: int, window size as described above
    Output:
        data: list of tuples (x, y). x is the id of the target word (the center word in current window) and y is the id of the context word
    '''
    # YOUR CODE HERE
    data=[]
    for i in PP_corpus:
      for j in range(len(i)):
        for k in range(1,window_size+1):
          if j-k >= 0:
            temp1=(i[j],i[j-k])
            data.append(temp1)
          if j+k < len(i):
            temp2=(i[j],i[j+k])
            data.append(temp2)          
    return data
    
data = data_gen(PP_corpus, 2)
df = pd.DataFrame(data, columns = ['input', 'label'])

PP_corpus

data

'''test for data_gen'''
def test_data_gen():
  assert df.shape == (66, 2)
  print('Test passed', '\U0001F44D')
test_data_gen()

"""# One-hot Encoding"""

import numpy as np


def to_one_hot_encoding(data_point_index, one_hot_dim):
    '''
    Input:
        data_point_index: integer value between 0 and one_hot_dim (index at which the one_hot_encoding array value will be 1 and 0 otherwise)
        one_hot_dim : int, vocabulary size
    Output:
        one_hot_encoding: np array of size (vocabulary size, ) containing one hot encoding
    '''
    # YOUR CODE HERE
    one_hot_encoding=np.zeros(one_hot_dim)
    one_hot_encoding[data_point_index]=1
    return one_hot_encoding

'''test for to_one_hot_encoding'''
def test_to_one_hot_encoding():
  arr = to_one_hot_encoding(4, len(unique_words))
  assert arr.tolist() == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
  print('Test passed', '\U0001F44D')
test_to_one_hot_encoding()

"""## Change  data into 1-hot encoding for Skip-gram Training"""

def one_hot_for_skip_gram(word2int, data):
    '''
    Input:
        word2int: dictionary, mapping from vocabulary words to ints
            data: list of tuples (x, y) list of tuples (x, y). x is the id of the target word (the center word in current window) and y is the id of the context word
    Output:
               X: numpy array of shape (samples, vocabulary_size) containing input words
               Y: numpy array of shape (samples, vocabulary_size) containing target words corresponding to input words in X
    '''
    # YOUR CODE HERE
    X=np.zeros((len(data),len(word2int)))
    Y=np.zeros((len(data),len(word2int)))
    for i in range(len(data)):
        a=to_one_hot_encoding(word2int[data[i][0]],len(word2int))
        X[i,:]=a
        b=to_one_hot_encoding(word2int[data[i][1]],len(word2int))
        Y[i,:]=b
    
    return X, Y
    
X_train,Y_train = one_hot_for_skip_gram(word2int, data)

Y_train

"""# Define Model Architecture
You could now train your model  using whatever optimizer you want.
In order to keep track of your training, you should also print out the loss every 3000 iterations.
Write your code in the cell below. Print out the loss every 3000 steps. Run your model for 20K epochs.
"""

'''test for Skip_gram_to_one_hot'''
def test_one_hot_for_skip_gram():
  assert Y_train.shape == (66,12)
  print('Test passed', '\U0001F44D')
test_one_hot_for_skip_gram()

"""![Skip Gram Model Architecture](https://cdncontribute.geeksforgeeks.org/wp-content/uploads/Skip-gram-architecture-2.jpg)

## Building skip gram network in Keras
Description of the Network
- There is only one hidden layer with 2 neurons and no activation
- Input and output layers have same shape as one-hot encoded vectors
- Output layer has activation softmax
- Loss used is categorical_crossentropy


Build this network using keras and train for at least 1000 epochs.
"""

def create_model():
    """
    Inputs:
        None
    Outputs:
        model: compiled keras model for skipgram architecture
    """
    # YOUR CODE HERE
    import keras
    from keras.layers import Input, Dense
    from keras.models import Model
    from keras import optimizers
    
    x= Input(shape=(len(word2int),))
    h=Dense(2,)(x)
    y=Dense(len(word2int),activation='softmax')(h)
    model=Model(inputs=x, outputs=y)
    model.compile(optimizer=optimizers.sgd(lr=0.01),loss='categorical_crossentropy',metrics=['accuracy'])
    model.summary()
    return model

def get_weights_and_bias(model, layer_index):
    """
    Inputs:
        model: compiled keras model
        layer_index: index of the layer
    Outputs:
        weights: weights of hidden layer
        biases: biases of the hidden layer
    """
    # YOUR CODE HERE
    weights,biases=model.layers[layer_index].get_weights()
    return weights, biases

"""Test for get_weights_and_bias"""
model = create_model()
w, b = get_weights_and_bias(model, 1)
assert w.shape[1] == 2
assert b.shape[0] == 2
print('Test passed', '\U0001F44D')

"""### Remember the model before training"""

import copy
model_before = copy.copy(model)

"""### Training"""

model.fit(X_train, Y_train, epochs = 1000, batch_size = 20)

"""## (1) Word embedding extraction <br>
Extract your word embedding matrix from the model and print out its shape.
(The size should be [vocabulary_size, embedding_dimension])
"""

def get_embeddings(model, flag):
    """
    Inputs:
        model: compiled keras model
        flag:int, {0 or 1}, if 0 represents input vectors else represents output vectors
    Outputs:
        embeddings: numpy array of shape(vocabulary_size, embedding_dimension), word embeddings of all words
    """
    # YOUR CODE HERE
    w,b=get_weights_and_bias(model,1)
    embeddings=model.layers[flag+1].get_weights()[0]
    
    return embeddings

embeddings_before = get_embeddings(model_before, 1)
embeddings_after_input = get_embeddings(model, 1).T
embeddings_after_output = get_embeddings(model, 0)

"""## (2) Visualization
<p>In this step, you need to visualize your word vectors by dimension reduction. (e.g. PCA or t-SNE)</p>
<p>If you are not satisfied with the quality of your word vector from visualization (in most cases), you could try to change some parameters in your model (e.g. vocabulary_size, embedding_dimension) and re-train your word embedding.</p>

Visualize the word vectors before and after training by changing vectors to either embeddings_before or embeddings_after.

Visulaize the word vectors of the learned input vectors and learned output vectors and see the difference.
"""

import matplotlib.pyplot as plt

## Set vectors
vectors = embeddings_after_input


# Build dataframe for vectors corrosponding to unique words where first column will be word.
w2v_df = pd.DataFrame(vectors, columns = ['x1', 'x2'])
w2v_df['word'] = unique_words
w2v_df = w2v_df[['word', 'x1', 'x2']]


# Plot the vectors
fig, ax = plt.subplots()

for word, x1, x2 in zip(w2v_df['word'], w2v_df['x1'], w2v_df['x2']):
    ax.annotate(word, (x1,x2), bbox={'facecolor':'red', 'alpha':0.5, 'pad':5})
    
# w2v_df = pd.DataFrame(vec_before, columns = ['x1', 'x2'])
# w2v_df['word'] = unique_words
# w2v_df = w2v_df[['word', 'x1', 'x2']]
# for word, x1, x2 in zip(w2v_df['word'], w2v_df['x1'], w2v_df['x2']):
#     ax.annotate(word, (x1,x2), bbox={'facecolor':'blue', 'alpha':0.5, 'pad':5})

    
PADDING = 1.0
x_axis_min = np.amin(vectors, axis=0)[0] - PADDING
y_axis_min = np.amin(vectors, axis=0)[1] - PADDING
x_axis_max = np.amax(vectors, axis=0)[0] + PADDING
y_axis_max = np.amax(vectors, axis=0)[1] + PADDING
 
plt.xlim(x_axis_min,x_axis_max)
plt.ylim(y_axis_min,y_axis_max)
plt.rcParams["figure.figsize"] = (10, 10)

plt.show()

import matplotlib.pyplot as plt

## Set vectors
vectors = embeddings_after_output


# Build dataframe for vectors corrosponding to unique words where first column will be word.
w2v_df = pd.DataFrame(vectors, columns = ['x1', 'x2'])
w2v_df['word'] = unique_words
w2v_df = w2v_df[['word', 'x1', 'x2']]


# Plot the vectors
fig, ax = plt.subplots()

for word, x1, x2 in zip(w2v_df['word'], w2v_df['x1'], w2v_df['x2']):
    ax.annotate(word, (x1,x2), bbox={'facecolor':'red', 'alpha':0.5, 'pad':5})
    
# w2v_df = pd.DataFrame(vec_before, columns = ['x1', 'x2'])
# w2v_df['word'] = unique_words
# w2v_df = w2v_df[['word', 'x1', 'x2']]
# for word, x1, x2 in zip(w2v_df['word'], w2v_df['x1'], w2v_df['x2']):
#     ax.annotate(word, (x1,x2), bbox={'facecolor':'blue', 'alpha':0.5, 'pad':5})

    
PADDING = 1.0
x_axis_min = np.amin(vectors, axis=0)[0] - PADDING
y_axis_min = np.amin(vectors, axis=0)[1] - PADDING
x_axis_max = np.amax(vectors, axis=0)[0] + PADDING
y_axis_max = np.amax(vectors, axis=0)[1] + PADDING
 
plt.xlim(x_axis_min,x_axis_max)
plt.ylim(y_axis_min,y_axis_max)
plt.rcParams["figure.figsize"] = (10, 10)

plt.show()



"""### Advanced Experiments
- Tune hyperparameters to see if you can get better representations
- Try to add more sentences using the same vocabulary (or expanding the vocabulary only slightly) to see if you can learn better representations
"""