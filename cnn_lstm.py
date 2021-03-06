# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import scipy
from scipy import misc
import glob
from PIL import Image
import os
import matplotlib.pyplot as plt
import librosa
from keras import layers
from keras.layers import (Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, 
                          Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D,Dropout)
from tensorflow.keras.layers import Dense,Dropout,Activation,Flatten
from keras.models import Model, load_model
from keras.preprocessing import image
from keras.utils import layer_utils
import pydot
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
#from keras.utils import plot_model
from tensorflow.keras.optimizers import Adam
from keras.initializers import glorot_uniform
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from keras.preprocessing.image import ImageDataGenerator
import random

z="/content/drive/MyDrive/project_adv/pos1/"
c=1
for i,filename in enumerate(os.listdir(z)):
  file_name = '/content/drive/MyDrive/project_adv/pos1/'+str(filename)
  y,sr = librosa.load(file_name,sr=None)   
  mels = librosa.feature.melspectrogram(y=y,sr=sr)
  fig = plt.Figure()
  canvas = FigureCanvas(fig)
  p = plt.imshow(librosa.power_to_db(mels,ref=np.mean))
  plt.savefig('/content/drive/MyDrive/project_adv/pos_imgs/'+str(c)+'.png')
  if(c>=245):
    break
  c+=1

z="/content/drive/MyDrive/project_adv/neg1/"
c=1
for i,filename in enumerate(os.listdir(z)):
  file_name = '/content/drive/MyDrive/project_adv/neg1/'+str(filename)
  y,sr = librosa.load(file_name,sr=None)   
  mels = librosa.feature.melspectrogram(y=y,sr=sr)
  fig = plt.Figure()
  canvas = FigureCanvas(fig)
  p = plt.imshow(librosa.power_to_db(mels,ref=np.mean))
  plt.savefig('/content/drive/MyDrive/project_adv/neg_imgs/'+str(c)+'.png')
  if(c>=300):
    break
  c+=1

src='/content/drive/MyDrive/project_adv/pos_imgs/'
des1='/content/drive/MyDrive/project_adv/test/pos/'
des2='/content/drive/MyDrive/project_adv/train/pos/'
c=1
for i,filename in enumerate(os.listdir(src)):
  file_name = '/content/drive/MyDrive/project_adv/pos_imgs/'+str(filename)
  if(c<37):
    shutil.copy(file_name,des1)
  else:
    shutil.copy(file_name,des2)
  c+=1

src='/content/drive/MyDrive/project_adv/neg_imgs/'
des1='/content/drive/MyDrive/project_adv/test/neg/'
des2='/content/drive/MyDrive/project_adv/train/neg/'
c=1
for i,filename in enumerate(os.listdir(src)):
  file_name = '/content/drive/MyDrive/project_adv/neg_imgs/'+str(filename)
  if(c<46):
    shutil.copy(file_name,des1)
  else:
    shutil.copy(file_name,des2)
  c+=1

train_dir = "/content/drive/MyDrive/project_adv/train/"
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(train_dir,target_size=(288,432),color_mode="rgba",class_mode='categorical',batch_size=128)

validation_dir = "/content/drive/MyDrive/project_adv/test/"
vali_datagen = ImageDataGenerator(rescale=1./255)
vali_generator = vali_datagen.flow_from_directory(validation_dir,target_size=(288,432),color_mode='rgba',class_mode='categorical',batch_size=128)

from keras.layers import Activation, Dense, Dropout, Conv2D, Flatten, MaxPooling2D, GlobalMaxPooling2D, GlobalAveragePooling1D, AveragePooling2D, Input, Add
from keras.models import Sequential

import cv2
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
import keras
from keras.models import Sequential, Model,load_model
#from keras.optimizers import SGD
from keras.callbacks import EarlyStopping,ModelCheckpoint
from google.colab.patches import cv2_imshow
from keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D,MaxPool2D
from keras.preprocessing import image
from keras.initializers import glorot_uniform
from tensorflow.keras.layers import LSTM, Dense
from keras.layers import TimeDistributed

model = Model(inputs=base_model.input, outputs=headModel)
es=EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=20)
#mc = ModelCheckpoint('/content/drive/MyDrive/resnet_50div_images/best_model1.h5', monitor='val_accuracy', mode='auto')
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
H = model.fit_generator(train_generator,validation_data=vali_generator,epochs=70,verbose=1)

import keras.backend as K
def get_f1(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val


opt = Adam(learning_rate=0.0005)
model.compile(optimizer = opt,loss='categorical_crossentropy',metrics=['accuracy',get_f1]) 

model.fit_generator(train_generator,epochs=70,validation_data=vali_generator)



model = Sequential()
input_shape = (288,432,4)#1st hidden layer
classes=2


model.add(TimeDistributed(Conv2D(8,kernel_size=(3,3),strides=(1,1),input_shape=input_shape)))
model.add(TimeDistributed(BatchNormalization(axis=3)))
model.add(TimeDistributed(Activation('relu')))
model.add(TimeDistributed(MaxPooling2D((2, 2))))


#2nd hidden layer
model.add(TimeDistributed(Conv2D(16,kernel_size=(3,3),strides=(1,1))))
model.add(TimeDistributed(BatchNormalization(axis=3)))
model.add(TimeDistributed(Activation('relu')))
model.add(TimeDistributed(MaxPooling2D((2, 2))))

#model.add(Conv2D(32,kernel_size=(3,3),strides=(1,1)))
#model.add(BatchNormalization(axis=3))
#model.add(Activation('relu'))
#model.add(MaxPooling2D((2, 2)))

model.add(TimeDistributed(Flatten()))
#model.add(Dropout(rate=0.5))#Output layer
#model.add(Dense(2,activation='softmax'))
model.add(LSTM(units = 50, return_sequences = True, input_shape = (56576,1)))
model.add(Dropout(0.2))

model.add(LSTM(units = 50, return_sequences = True))

model.add(Dense(50, activation='relu'))
model.add(LSTM(units = 50, return_sequences = True))
#regressor.add(Dropout(0.2))
model.add(LSTM(units = 50))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))


import keras.backend as K
def get_f1(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

opt = Adam(learning_rate=0.0005)
model.compile(optimizer = opt,loss='categorical_crossentropy',metrics=['accuracy',get_f1]) 

model.fit_generator(train_generator,epochs=70,validation_data=vali_generator)

from google.colab import drive
drive.mount('/content/drive')