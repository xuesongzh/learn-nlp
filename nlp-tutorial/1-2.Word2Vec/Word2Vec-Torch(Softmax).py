# -*- coding: utf-8 -*-
"""“Word2Vec-Torch(Softmax).ipynb”的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rKNaAZwe3tdZMzKjOX6gP8nrQBhKxbFa
"""

'''
  code by Tae Hwan Jung(Jeff Jung) @graykode, modify by wmathor
'''
import torch
import numpy as np
import torch.nn as nn
import torch.optim as optimizer
import torch.utils.data as Data

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
dtype = torch.FloatTensor

sentences = ["jack like dog", "jack like cat", "jack like animal",
  "dog cat animal", "banana apple cat dog like", "dog fish milk like",
  "dog cat animal like", "jack like apple", "apple like", "jack like banana",
  "apple banana jack movie book music like", "cat dog hate", "cat dog like"]
sentence_list = " ".join(sentences).split() # ['jack', 'like', 'dog']
vocab = list(set(sentence_list))
word2idx = {w:i for i, w in enumerate(vocab)}
vocab_size = len(vocab)

# model parameters
C = 2 # window size
batch_size = 8
m = 2 # word embedding dim

skip_grams = []
for idx in range(C, len(sentence_list) - C):
  center = word2idx[sentence_list[idx]]
  context_idx = list(range(idx - C, idx)) + list(range(idx + 1, idx + C + 1))
  context = [word2idx[sentence_list[i]] for i in context_idx]

  for w in context:
    skip_grams.append([center, w])

def make_data(skip_grams):
  input_data = []
  output_data = []
  for a, b in skip_grams:
    input_data.append(np.eye(vocab_size)[a])
    output_data.append(b)
  return input_data, output_data

input_data, output_data = make_data(skip_grams)
input_data, output_data = torch.Tensor(input_data), torch.LongTensor(output_data)
dataset = Data.TensorDataset(input_data, output_data)
loader = Data.DataLoader(dataset, batch_size, True)

class Word2Vec(nn.Module):
  def __init__(self):
    super(Word2Vec, self).__init__()
    self.W = nn.Parameter(torch.randn(vocab_size, m).type(dtype))
    self.V = nn.Parameter(torch.randn(m, vocab_size).type(dtype))

  def forward(self, X):
    # X : [batch_size, vocab_size]
    hidden = torch.mm(X, self.W) # [batch_size, m]
    output = torch.mm(hidden, self.V) # [batch_size, vocab_size]
    return output

model = Word2Vec().to(device)
loss_fn = nn.CrossEntropyLoss().to(device)
optim = optimizer.Adam(model.parameters(), lr=1e-3)

for epoch in range(2000):
  for i, (batch_x, batch_y) in enumerate(loader):
    batch_x = batch_x.to(device)
    batch_y = batch_y.to(device)
    pred = model(batch_x)
    loss = loss_fn(pred, batch_y)

    if (epoch + 1) % 1000 == 0:
      print(epoch + 1, i, loss.item())
    
    optim.zero_grad()
    loss.backward()
    optim.step()

import matplotlib.pyplot as plt
for i, label in enumerate(vocab):
  W, WT = model.parameters()
  x,y = float(W[i][0]), float(W[i][1])
  plt.scatter(x, y)
  plt.annotate(label, xy=(x, y), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom')
plt.show()

