import cv2
import numpy as np

def makeImgs(data):
    for i in range(len(data)):
        image = np.zeros((64,64,1), np.uint8)
        scaled = [data[i][x]*255/16 for x in range(64)]
        for x in range(8):
            for y in range(8):
                image[x*8:x*8+7,y*8:y*8+7]
        cv2.imwrite("img"+str(i)+".jpg", image)