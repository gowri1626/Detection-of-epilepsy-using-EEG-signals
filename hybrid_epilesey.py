from google.colab import drive
drive.mount('/content/drive')

import zipfile
#source files are downloaded from "UNIVERSITY OF BONN"

source_zip1 = '/content/drive/MyDrive/epilepsey/f.zip'
source_zip2='/content/drive/MyDrive/epilepsey/n.zip'
source_zip3='/content/drive/MyDrive/epilepsey/o.zip'
source_zip4='/content/drive/MyDrive/epilepsey/s.zip'
source_zip5='/content/drive/MyDrive/epilepsey/z.zip'
dest='/content/drive/MyDrive/epilepsey/dataset'

with zipfile.ZipFile(source_zip1,'r') as zip:
  zip.extractall(dest)

with zipfile.ZipFile(source_zip2,'r') as zip:
  zip.extractall(dest)

with zipfile.ZipFile(source_zip3,'r') as zip:
  zip.extractall(dest)

with zipfile.ZipFile(source_zip4,'r') as zip:
  zip.extractall(dest)

with zipfile.ZipFile(source_zip5,'r') as zip:
  zip.extractall(dest)

DATA_A='/content/drive/MyDrive/epilepsey/dataset/Z/'
DATA_B='/content/drive/MyDrive/epilepsey/dataset/O/'
DATA_C='/content/drive/MyDrive/epilepsey/dataset/N/'
DATA_D='/content/drive/MyDrive/epilepsey/dataset/F/'
DATA_E='/content/drive/MyDrive/epilepsey/dataset/S/'

!pip install tqdm
import os
from tqdm import tqdm

import pandas as pd
import glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv

LABEL1 = 0
LABEL2 = 1
LABEL3 = 2

def load():
      datafiles = []
      nFiles=0
      for fn in tqdm(os.listdir(DATA_A)):
              i =np.loadtxt(DATA_A +fn)
              datafiles.append([i,np.array(LABEL1)])
              nFiles+=1

      for fn in tqdm(os.listdir(DATA_B)):
              i =np.loadtxt(DATA_B +fn)
              datafiles.append([i,np.array(LABEL1)])
              nFiles+=1

      for fn in tqdm(os.listdir(DATA_C)):
              i =np.loadtxt(DATA_C +fn)
              datafiles.append([i,np.array(LABEL2)])
              nFiles+=1

      for fn in tqdm(os.listdir(DATA_D)):
              i =np.loadtxt(DATA_D +fn)
              datafiles.append([i,np.array(LABEL2)])
              nFiles+=1

      for fn in tqdm(os.listdir(DATA_E)):
              i =np.loadtxt(DATA_E +fn)
              datafiles.append([i,np.array(LABEL3)])
              nFiles+=1
      return datafiles

data =load()
print(len(data),"Files")

from sklearn.utils import shuffle
from keras.utils import to_categorical

data = shuffle(data)

n_train =round(len(data)*0.8)
train_data = data[0:n_train]
test_data=data[n_train:]

X_train = np.array([d[0] for d in train_data])
Y_train = np.array([d[1] for d in train_data])

X_test = np.array([d[0] for d in test_data])
Y_test = np.array([d[1] for d in test_data])

X_train.shape

X_train = X_train.reshape(X_train.shape[0], 4097, 1)
Y_train = Y_train.reshape(Y_train.shape[0],1)
Y_train = to_categorical(Y_train, num_classes = 3)

X_test = X_test.reshape(X_test.shape[0], 4097, 1)
Y_test = Y_test.reshape(Y_test.shape[0],1)
Y_test = to_categorical(Y_test, num_classes = 3)

from keras.layers import Flatten

# Hybrid model = CNN+LSTM
hidden_size = 32
model = Sequential()


model.add(Convolution1D(64, 10, strides=2, padding='valid', activation='relu',input_shape=(4097,1)))
model.add(Dropout(0.2))
model.add(MaxPooling1D(3))

model.add(Convolution1D(32 ,5, strides=2, padding='valid', activation='relu'))
model.add(Dropout(0.2))
model.add(MaxPooling1D(3))

model.add(Convolution1D(16, 4, strides=1, padding='valid', activation='relu'))
model.add(Dropout(0.2))
model.add(MaxPooling1D(3))

model.add(Dense(32))
model.add(Activation('relu'))

model.add(LSTM(hidden_size))
model.add(Dropout(0.3))

model.add(Flatten())
model.add(Dense(3, activation='softmax'))

batch_size = 4
n_epoch = 20
use_dropout = True

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['mae', 'acc'])

print(model.summary())

history = model.fit(X_train, Y_train, validation_split=0.2, batch_size=batch_size, epochs=n_epoch)
score = model.evaluate(X_test, Y_test, batch_size=batch_size)

print(history.history.keys())

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend ([ 'train', 'test'], loc= 'upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend ([ 'train', 'test'], loc= 'upper left')
plt.show()

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score, f1_score

Y_pred=model.predict(X_test)
Y_pred= np.round(Y_pred)

#print(Y_pred)

cm = confusion_matrix(Y_test.argmax(axis=1),Y_pred.argmax(axis=1))
print(cm)
print(classification_report (Y_test, Y_pred))
print(round((accuracy_score (Y_test, Y_pred)*100),2))
print(round (f1_score (Y_test, Y_pred, average='weighted'), 3))
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()
