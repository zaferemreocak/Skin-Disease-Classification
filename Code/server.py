from keras.models import load_model

loadingModule = 'savedModel1.h5'

print("Loading module: ", loadingModule)

classifier = load_model(loadingModule)

import socket

# create a socket object
serversocket = socket.socket() 

# get local machine name
host = "localhost" #socket.gethostname()                           

port = 9993                                         

print("Server is starting on ", host, ":", port)

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)        
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img,image                                   

print("Server is started!")

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()      

    print("Client (%s) is connected!" % str(addr))
    
    while True:
	    data = clientsocket.recv(1024) #.decode('UTF-8')
	    print(data)
	    test_image = image.load_img(data, target_size = (64, 64))
	    test_image = image.img_to_array(test_image)
	    test_image = np.expand_dims(test_image, axis = 0)
	    test_image *=1.0/255
	    result = classifier.predict(test_image)
	    print(result[0][0])
	    clientsocket.send(str(result[0][0]).encode())
    clientsocket.close()

