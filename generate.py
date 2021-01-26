import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt 
from tensorflow import keras
from tensorflow.keras.models import load_model
 
def trainIt():
  new_model=load_model('cnn.h5')
  data=[]
  modele = load_model('generator.h5')
  for i in range(300):
    vector = np.random.normal(0,1, (100,100))
    X = modele.predict(vector)
    data.append(np.asarray(X))
  y=data[0]
  y.resize((28,28),refcheck=False)
  data[0].resize((100,28,28,1),refcheck=False)
  pred=new_model.predict(data[0])
  print(np.argmax(pred[0]))

  listeOfPrediction=[]
  for i in range(150):
    pred=new_model.predict(data[i])
    if (np.argmax(pred[0]))!=0:
     listeOfPrediction.append(np.argmax(pred[0]))

  return listeOfPrediction

bord=[[0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0]]
     
def allowed(x,y,val):
    for i in range(9):
       if (bord[x][i]==val ): 
         return False
    for j in range(9):
      if (bord[j][y]==val):
          return False 
    xi=(x//3)*3
    yi=(y//3)*3
    for i in range(0,3):
       for j in range(0,3):
         if (bord[xi+i][yi+j]==val):
           return False
    return True

def matrice():
  count=0
  listeOfPrediction=trainIt()
  while count<38 :
    row=np.random.randint(9)
    column=np.random.randint(9)
    rand=np.random.randint(0,len(listeOfPrediction))  
    print(allowed(row,column,listeOfPrediction[rand])) 
    if allowed(row,column,listeOfPrediction[rand]) ==True  :
     print(bord[row][column])
     if bord[row][column] == 0 :
      count=count+1
      bord[row][column]=listeOfPrediction[rand]
  nbr=0
  for i in range(9):
    for j in range(9):
      if(bord[i][j]!=0) :
        nbr=nbr+1      
  print(np.matrix(bord))
  print(nbr)
  return bord