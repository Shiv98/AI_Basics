# -*- coding: utf-8 -*-
"""Shivangi Gupta - nlp_quiz1_f.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jFTt79LrnJPAmAE_19i55XZqM_KdeXKK
"""

import numpy as np

"""## Basic Text Processing
### Loading dataset
You need not mess with this code. Just run these cells to download the data.
"""

!wget https://raw.githubusercontent.com/krishnamrith12/NotebooksNLP/master/Data/Tokenization/Chat1.txt

import string
import matplotlib.pyplot as plt
import nltk
print('***********************************************************')
print('Your data successfully loaded.')
print('First 10 lines of conversation is shown:')
print('This is conversation between machine and user.')
print('***********************************************************')
with open("./Chat1.txt") as myfile:
  for x in range(0,10):
    print(next(myfile))

"""### Tokenize the data

Suppose you are doing operations on string data named '*str = I love CODING.*'

1.   Tokenize the data. For eg, output after this step will be ['I', 'love', 'CODING.']
2.   Lowercase the data . For ex, your output will be ['i' ,'love', 'coding.']
3. Remove the puctuations from data using . For eg, you will get output as ['i' ,'love', 'coding'] (Full stop is removed here). We have provided list of puctuations. So make sure that you remove all the punctuations.
"""

f = open('./Chat1.txt','r')
content=f.read()

# Punctuation list is as follows:
punc_list =['.',',',':','!','?','(',')',';']

def tokenize(raw_data):
  """
  Inputs:
    raw_data: string, raw text of the corpus
  Outputs:
    tokenized_data: list of strings, split raw_data on whitespace  
  """
  # YOUR CODE HERE
  tokenized_data=raw_data.split()
  return tokenized_data

tokenized_data = tokenize(content)

"""Test tokenize"""
def test_tokenize():
  assert(tokenized_data[0:5] == ['User:', 'So', "how's", 'it', 'going?'])
  assert(len(tokenized_data) == 1013)
  print('Test passed', '\U0001F44D')
test_tokenize()

def lowercase_data(word):
  """
  Inputs:
    word: a string
  Outputs:
    word_lowercase: a string (all alphabets in lowercase)
  """
  # YOUR CODE HERE
  word_lowercase=word.lower()
  return word_lowercase

"""Test lowercase_data"""
def test_lowercase_data():
  assert(lowercase_data('Machine LEArning is AWesome;') == 'machine learning is awesome;')
  print('Test passed', '\U0001F44D')
test_lowercase_data()

def remove_punctuation(word, punc_list):
  '''
  Inputs:
    punc_list: a list (containing punctuation characters)
    word: a string
  Outputs:
    word_no_punc: a string (without any punctuation characters)
  '''
  # YOUR CODE HERE
  word_no_punc=""  
  for i in word:
    if i not in punc_list:
      word_no_punc=word_no_punc + i
      
  return word_no_punc

"""Test remove_punctuation"""
def test_remove_punctuation():
  assert(remove_punctuation('mac.hin;e le,ar.ning is? awe!some;', punc_list) == 'machine learning is awesome')
  assert(remove_punctuation(tokenized_data[4], punc_list) == 'going')
  print('Test passed', '\U0001F44D')
test_remove_punctuation()

def preprocess(content):
  """
  Inputs:
    content: a string
  Outputs:
    wordlist: a list of strings
    
  Action:
    1. Preprocess the string 'content' using the functions created above (tokenize, lowercase and remove_punctuation) 
    2. Store it in a list 'wordlist'
    
  """
  # YOUR CODE HERE
  lower=lowercase_data(content)
  rem=remove_punctuation(lower, punc_list)
  wordlist=tokenize(rem)
  #print(wordlist)
  return wordlist

wordlist = preprocess(content)

"""Test preprocess"""
def test_preprocess():
  assert(len(wordlist) == 1013)
  print('Test passed', '\U0001F44D')
test_preprocess()

"""### Plot the frequency of words
You need to plot the frequncy of words using function provided. <br>
"""

def plot_frequency(y):
  N = len(y)
  x = range(N)
  width = 1/0.5
  plt.bar(x, y, width, color="blue")
  plt.show()

"""### To do
1) Find out count of each word using  function and store this  in list named word_count using <br>
2) Pass the word_count list to function to plot the frequency plot.
"""

def frequency(wordlist):
  """
  Inputs:
    wordlist: a list of string
  Outputs:
    word_count: a list, frequency of all the items in wordlist
  """
  # YOUR CODE HERE
  temp=[]
  word_count=[]
  count=0
  for i in wordlist:
    if i not in temp:
      temp.append(i)
  for j in range(0, len(temp)):
    word_count.append(wordlist.count(temp[j]))
   
  return word_count

word_count = frequency(wordlist)
plot_frequency(word_count)

"""Test frequency

## (1) Cosine Similarity
When we have word vectors, we need a way to quantify the similarity between individual words, according to these vectors. One such metric is cosine-similarity. We will be using this to find words that are "close" and "far" from one another.

We can think of n-dimensional vectors as points in n-dimensional space. If we take this perspective, *L1* and *L2* Distances help quantify the amount of space "*we must travel"* to get between these two points. 

Another approach is to examine the angle between two vectors. Instead of computing the actual angle, we can leave the similarity in terms of  similarity=cos(Θ) . Formally, the Cosine Similarity  s  between two vectors  p  and  q  is defined as:

$s = \frac{p⋅q}{||p||||q||} $, where s∈[−1,1]<br>
You need to implement this function.
"""

import math
def cosine_similarity(v1,v2):
    """
    Input:
        v1: list of floats,
        v2: list of floats, same length as v1
        
    Output:
        cs: single floating point value, cosine similarity of v1 and v2 as defined above
        /
    """
    # YOUR CODE HERE
    v1=np.array(v1)
    v2=np.array(v2)
    cs = v1.dot(v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    return cs

'''test for cosine_similarity'''
v1,v2 = [3, 45, 7, 2], [2, 5.4, 13, 15]
v = cosine_similarity(v1,v2)
assert np.isclose(v, 0.39187288174224344, 0.0001)

print('Test passed', '\U0001F44D')

"""### Most similar word
Implement the function, given a word "*x*", it will return most similar word from first column of data, based on similarity measure. <br>
For example, for most similar word to *king* could be *man*. <br>
"""

def most_similar(input_word,wordvec_dict):
  """
  Input:
      input_word: any word
      wordvec_dict: dictionary of word vectors(list of floats), where a word is the key and its word_vector is the value
      
  Output:
      out: string, the word in wordvec_dict most similar to 'word'
  """
  # YOUR CODE HERE
  v1=wordvec_dict.get(input_word)
  temp=[]
  tempkeys=list(wordvec_dict.keys())
  tempkeys.remove(input_word)
  for v2 in wordvec_dict.values():
    if v2 != v1:
      val= cosine_similarity(v1,v2)  
      temp.append(val)
    
    else: 
      pass
  maxpos = temp.index(max(temp))  
  out =tempkeys[maxpos] 
  return out

word_vec_dict = {
    'princess': [-1.720603,	-3.560657],
    'queen': [-0.722603,	-1.232549],
    'man':	[-0.370373,	0.576843],
    'boy':	[-1.693504,	0.719822]

}
most_similar('boy', word_vec_dict)

word_vec_dict = {
    'princess': [-1.720603,	-3.560657],
    'queen': [-0.722603,	-1.232549],
    'man':	[-0.370373,	0.576843],
    'boy':	[-1.693504,	0.719822]

}

'''test for most_similar'''
assert most_similar('queen', word_vec_dict) == 'princess'
print('Test passed', '\U0001F44D')

