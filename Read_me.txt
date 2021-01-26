Note :
The files are diviside by fonction d'activation we trining our modele with different fonction 
d'activation recommended for gans (leakyrelu,relu,elu) and in this file we chosse just leakyrelu and 
relu for the hidden layer because for the output layer we chosse sigmoid and tanh 
to just make the different and the impact of differences between the two.
and in every file we have different archicture depending of the number of hidden layer in 
each one (discriminator and generateor)
we start with 1 hidden layer of the both until three (in some cases four depending on the modele) hidden 
layer after we try different hidden layer for each one to see the impact
for the learning rate we try different one with different batch size .
all that with the adam optimmizer
because he give better results then the other but that did avoid to try other one,so we chosse 
the best archi and try it with sgd and rmsprop and adadelta 
our choice of best architecture is was based on the image generated in the training with epoch=10K and the losses and the fid 
for the last file we added "some_echecs_happend" contain some problems happen when training gans .
at the end we add another file who is not good organized but he just contains values exesiting in rapport
binome:
Hammouche Manel Yasmine
Bnedjoudi Meriem