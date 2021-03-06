# -*- coding: utf-8 -*-
"""Copie de Untitled38.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1abgC_8BwWbfWFQepbyLsz3OHjUqO25Yw
"""

# Commented out IPython magic to ensure Python compatibility.
import tensorflow as tf
import numpy as np
from numpy import cov,trace,iscomplexobj,asarray
from numpy.random import shuffle
from scipy.linalg import sqrtm
from keras.applications.inception_v3 import InceptionV3,preprocess_input
from tensorflow.keras.datasets.mnist import load_data
from skimage.transform import resize
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input 
from tensorflow.keras.models import Sequential, Model
from random import randint
import matplotlib.pyplot as plt 
import os
from tensorflow.keras.models import load_model
from numpy.random import randint,shuffle
from scipy.linalg import sqrtm
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from skimage.transform import resize
from tensorflow.keras.datasets import mnist
import cv2 
from tensorflow.keras.models import load_model
from keras.utils.vis_utils import plot_model 
losses = []
accuarcys=[]
FIDListe=[]
listeTrain=[]
def scale_images(images, new_shape):
 #redemensionne avec le plus proche voisin apres sauvgarde 
 imageList = list()
 for i in images:
  new_image = resize(i, new_shape, 0)
  
  imageList.append(new_image)
 return asarray(imageList)
def calculate_fid(model, images1, images2): 
  act1 = model.predict(images1)
  act2 = model.predict(images2)
  mu1, sigma1 = act1.mean(axis=0), cov(act1, rowvar=False)
  mu2, sigma2 = act2.mean(axis=0), cov(act2, rowvar=False)
  ssdiff = np.sum((mu1 - mu2)**2.0)
  covmean = sqrtm(sigma1.dot(sigma2))
  if iscomplexobj(covmean):
    covmean = covmean.real
  fid = ssdiff + trace(sigma1 + sigma2 - 2.0 * covmean)
  return fid
def Discriminator(shape=(28,28,1)):  
     
    model = Sequential()
    model.add(tf.keras.layers.Flatten(input_shape=shape))
    model.add(tf.keras.layers.Dense(block_size*4, input_shape=shape))
    model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
    model.add(tf.keras.layers.Dense(block_size*2, input_shape=shape))
    model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
    
    model.add(tf.keras.layers.Dense(block_size, input_shape=shape))
    model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
    model.add(tf.keras.layers.Dense(block_size/2, input_shape=shape))
    model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    model.summary()
    return model
def Generator(latent_space_size):
        
        model = Sequential()
        
        model.add(tf.keras.layers.Dense(block_size/2, input_dim=latent_space_size) ) 
        model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
        model.add(tf.keras.layers.BatchNormalization(momentum=0.8))
        
        model.add(tf.keras.layers.Dense(block_size))
        model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
        model.add(tf.keras.layers.BatchNormalization(momentum=0.8))
        
       
        model.add(tf.keras.layers.Dense(block_size*2))
        model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
        model.add(tf.keras.layers.BatchNormalization(momentum=0.8))



        model.add(tf.keras.layers.Dense(block_size*4))
        model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
        model.add(tf.keras.layers.BatchNormalization(momentum=0.8))
        
        model.add(tf.keras.layers.Dense(28 * 28 * 1, activation='tanh'))
        model.add(tf.keras.layers.Reshape((28, 28, 1)))
        model.summary()
        return model 
def GAN(gen,dis): 
       model=Sequential() #a sequential model combien discr and generator
       # to train the generator later
       model.add(gen)
       model.add(dis) 
       model.summary()
       return model
 

def smooth_positive_labels(y):
  # smoothing real to [0.7, 1.2]
      #print("y ",y)
      rand=np.random.random_sample(y.shape)
      #print("y rand" ,rand)
      y= y - 0.3 + (rand * 0.5)
      #print("positive label " ,y)
      return y

def smooth_negative_labels(y):
  #smoothing fake to [0.0,0.3]
     return y+ np.random.random_sample(y.shape)*0.3   
 
def train(Generator,Discriminator,GAN,BATCH_SIZE,EPOCHS):
    (X_train,Y_train), (X_test,Y_test) = mnist.load_data()
    X_train=(X_train- 127.5) / 127.5 #[-1,1]
    X_train = np.expand_dims(X_train, axis=3)
    X_test=(X_test- 127.5) / 127.5 #[-1,1]
    X_test = np.expand_dims(X_test, axis=3)
     #rescale image to shape (60000,28,28,1)
    real=np.ones((BATCH_SIZE,1)) #a vector of 1  for real
    fake=np.zeros((BATCH_SIZE,1)) #for fake 0
    real=smooth_positive_labels(real)
    print("real one : ", real.shape, real.min(), real.max())
    fake=smooth_negative_labels(fake)
    print("fake one:" ,fake.shape, fake.min(), fake.max())
   
    for e in range(EPOCHS):
      X=np.random.randint(0,X_train.shape[0],BATCH_SIZE)
      real_image=X_train[X]  
       
      noise=np.random.normal(0,1, (BATCH_SIZE,LATENT_SPACE_SIZE))
      generated_image=Generator.predict(noise)
       
      discriminator_real_loss=Discriminator.train_on_batch(real_image,real)
      discriminator_fake_loss=Discriminator.train_on_batch(generated_image,fake)
      discriminator_loss,accuarcy=0.5*np.add(discriminator_real_loss,discriminator_fake_loss)
      noise=np.random.normal(0,1, (BATCH_SIZE,LATENT_SPACE_SIZE))
      generator_loss=GAN.train_on_batch(noise,real) 
      print("%d [Discriminator loss: %.4f%%][Generator loss: %.4f%% ]"
        %(e, discriminator_loss, generator_loss))
      if e % CHECKPOINT == 0:   
        sample_images(Generator,e) 
        losses.append((discriminator_loss,generator_loss))
        accuarcys.append(accuarcy)
        Generator.save(os.path.join("generator.h5"))
        images1=generated_image[:128] 
        images2=X_test[:128]
        print('Loaded', images1.shape, images2.shape)
        model1 = InceptionV3(include_top=False, pooling='avg', input_shape=(299,299,3))
        images1 = scale_images(images1 , (299,299,3))
        images2 = scale_images(images2, (299,299,3))
        print('Scaled', images1.shape, images2.shape)
        images1 = preprocess_input(images1)
        images2 = preprocess_input(images2)
        fid = calculate_fid(model1, images1, images2)
        print('FID: %.3f' % fid)
        FIDListe.append(fid)
      
    return  
 
def sample_images(Generator,epoch):
        r, c = 5, 5
        noise=np.random.normal(0,1, (BATCH_SIZE,LATENT_SPACE_SIZE))
        gen_imgs = Generator.predict(noise)

        # Rescale images 0 - 1
        gen_imgs = 0.5 * gen_imgs + 0.5

        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[i,j].imshow(gen_imgs[cnt, :,:,0],cmap='gray' )
                axs[i,j].axis('off')
                cnt += 1
        fig.savefig("sample_data/"+str(epoch)+".png")
        plt.close()


LATENT_SPACE_SIZE = 100
CHECKPOINT = 1000
BATCH_SIZE=128 
block_size=256
dis=Discriminator()
dis.compile(loss='binary_crossentropy',optimizer=Adam(learning_rate=0.0002,beta_1=0.5), metrics=['accuracy'] )
gen=Generator(LATENT_SPACE_SIZE)
dis.trainable=False
gan=GAN(gen,dis)
gan.compile(loss='binary_crossentropy',optimizer=Adam(lr=0.0002, beta_1=0.5))
train(Generator=gen,Discriminator=dis,GAN=gan,BATCH_SIZE=128,EPOCHS=10001 )

FIDListe = np.array(FIDListe)
#plt.plot(losses.T[0], label='Discriminator')
plt.plot(FIDListe, label='Generator')
plt.title("Training FID")
plt.xlabel("iterations")
plt.ylabel("FID")
plt.legend()
plt.show()

losses = np.array(losses)
plt.plot(losses.T[0], label='Discriminator')
plt.plot(losses.T[1], label='Generator')
plt.title("Training losses")
plt.xlabel("iterations")
plt.ylabel("losses")
plt.legend()
plt.show()

list_of_pics = list()
data=[]
model = load_model('generator.h5')
for i in range(1000):
  vector = np.random.normal(0,1, (100,100))
  X = model.predict(vector)
  X.resize(28,28)
  data.append(np.asarray(X))
 
new_array = np.array(data)
print(new_array.shape)
plt.imshow(new_array[9])

for i in range(0, 9):
    plt.subplot(331+i)
     # plot of 3 rows and 3 columns
    plt.axis('off') # turn off axis
    plt.imshow(new_array[i], cmap='gray_r')

plt.imshow(new_array[11],cmap='gray_r')

(X_train,Y_train),(X_test,Y_test)= mnist.load_data()
model1 = InceptionV3(include_top=False, pooling='avg', input_shape=(299,299,3))
print('Loaded', new_array[:100].shape, X_test[:100].shape)
images1=new_array[:100]
images2=X_test[:100]

images1 = scale_images(images1, (299,299,3))
images2 = scale_images(images2, (299,299,3))
print('Scaled', images1.shape, images2.shape)
# pre-process images
images1 = preprocess_input(images1)

images2 = preprocess_input(images2)

# calculate fid
fid = calculate_fid(model1, images1, images2)
print('FID: %.3f' % fid)