import cv2
import numpy as np
import time
import tensorflow as tf
from tensorflow.keras.models import load_model
import json
from solver import solver
def crop_center(img,cropx,cropy):
    y,x = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)    
    return img[starty:starty+cropy,startx:startx+cropx]
def predict_alphabet(ROI):
    
    alphabets_mapper = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}
    ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    ROI = cv2.threshold(ROI,225,255, cv2.THRESH_BINARY)[1]

    #Phone: 40x40
    #Laptop: 25x25

    ROI = crop_center(ROI, 50, 50)

    ROI_mo = cv2.resize(ROI, (28, 28))
    kernel = np.ones((2,2),np.uint8)
    ROI_mo = cv2.dilate(ROI_mo,kernel,iterations = 1)

    ROI_mo = ROI_mo.reshape(1, 28, 28, 1)
    ROI_mo = ROI_mo/255.0
    pred = model.predict(ROI_mo)
    probabilityValue = np.amax(pred)
    pred = np.argmax(pred, axis=-1)
    return alphabets_mapper[pred[0]]

def predict_color(ROI):
    
    colors = {0: "grey", 1: "yellow", 2: "green"}
    RGB = (np.asarray(ROI)[0][0])
    color_pred = co_model.predict(np.array([RGB]))
    color_pred = list(list(color_pred.astype(int))[0])
    color_index = color_pred.index(max(color_pred))
    return colors[color_index], RGB
    

file = 'Wordles/lolwordle.png'
image = cv2.imread(file)

image = cv2.resize(image, (412, 365))



model = load_model('Models/my_model.h5')
co_model = load_model('Models/color.h5')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#blur = cv2.medianBlur(gray, 5)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(gray, -1, sharpen_kernel)

thresh = cv2.threshold(sharpen,225,255, cv2.THRESH_BINARY_INV)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

image_number = 0
cnts = cnts[::-1]
letters = []

data_words = []
temp = []

for c in cnts:
    area = cv2.contourArea(c)
    if area > 800:
        x,y,w,h = cv2.boundingRect(c)
        ROI = image[y:y+h, x:x+w]
        ROI = cv2.resize(ROI, (68, 68))
        cv2.imwrite('Alphabets/ROI_{}.png'.format(image_number), ROI)

        final_color, RGB = predict_color(ROI)
        alphabet = predict_alphabet(ROI)
        letters.append(alphabet.lower())

        #data.append((alphabet.lower(), final_color))
        temp.append((alphabet.lower(), final_color))
        if len(temp) == 5:
            temp_word=""
            for i in temp:
                temp_word += i[0]
            if temp_word.find("nnn") == -1:
                data_words.append(temp)
            temp = []
            
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (255,0,0), 2)
        image_number += 1

#cv2.imshow("Contours detected in the Image", image)
"""
file = open("dictionary.json")
data = json.load(file)
data = list(data.keys())
x = [i for i in data if len(i) == 5]
choose_words = []
no_list = [i[0] for i in data_words if i[1] == "grey"]

   """         
print(data_words)           
solver(data_words, 5)
        
