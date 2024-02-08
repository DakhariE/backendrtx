#This code splits videos into frames. 

#This code is to split any mp4 video into frames3
import cv2
import numpy as np
import os

# This chooses video to captue
cap = cv2.VideoCapture('vid511x0.mkv')

# Makes a folder to store images
try:
    if not os.path.exists('data511'):
        os.makedirs('data511')
except OSError:
    print("Error: creating dir of photodata")

currentFrame = 0

while(True):
    #ret checks if there is a frame, frame is the actual frame as an image.
    ret, frame = cap.read()
    #This if statement gets every 100 frames.
    if currentFrame % 100 == 0:
        name= "./data511/frame" + str(int(currentFrame/100)) + '.jpg'
        print('Creating... ' + name)
        cv2.imwrite(name,frame)

    currentFrame += 1

    #if there are no more frames break
    if ret == False:
        break
#This stops video and closes any cv2 windows open.
cap.release()
cv2.destroyAllWindows()
