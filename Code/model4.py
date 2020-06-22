# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 10:27:47 2018

@author: HP
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 13:37:59 2018

@author: HP
"""

# Convolutional Neural Network

# Installing Theano
# pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git

# Installing Tensorflow
# pip install tensorflow

# Installing Keras
# pip install --upgrade keras

# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Intialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))

classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a third convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 1, activation = 'sigmoid'))


# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images

import h5py

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)


training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

classifier.fit_generator(training_set,
                         steps_per_epoch = 3217,
                         epochs = 10,
                         validation_data = test_set,
                         validation_steps = 792)


classifier.save("savedModel4.h5")


import numpy as np
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img,image
test_image = image.load_img('dataset/single_prediction/benigne_test.jpg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
test_image *=1.0/255
result = classifier.predict(test_image)
print(training_set.class_indices)
print(result[0][0])
if result[0][0] > 0.5:
    prediction = 'Melignant'
    print(prediction)
    file = open("report.txt","a")
    file.write("Accurancy : "+str(result[0][0])+" "+prediction+"---->"+"Attribute : Conv , Conv , Pooling , Conv , Conv , Pooling , Conv , Conv , Pooling , Flatten ,Fully Conn, Correct Result :Benigne Epoch: 10\n\n")
    file.close()
else:
    prediction = 'benigne'
    print(prediction)
    file = open("report.txt","a")
    file.write("Accurancy : "+str(result[0][0])+" "+prediction+"---->"+"Attribute : Conv , Conv , Pooling , Conv , Conv , Pooling , Conv , Conv , Pooling , Flatten ,Fully Conn, Correct Result :Benigne Epoch: 10\n\n")
    file.close()

