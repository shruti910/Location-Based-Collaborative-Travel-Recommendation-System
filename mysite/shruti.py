import numpy as np
import cv2

img = cv2.imread('priya_1405210039_input.jpg')
res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('gray' , res)

kernel = np.array([[-1,-1,-1],[2,2,2],[-1,-1,-1]])
kernel2 = np.array([[-1,2,-1],[-1,2,-1],[-1,2,-1]])

smoothed = cv2.filter2D(res,-1,kernel)
smoothed2 = cv2.filter2D(res,-1,kernel2)
kernel3 = np.ones((3,3),np.float32)/9
s = cv2.filter2D(smoothed2,-1,kernel3)
s2 = cv2.filter2D(smoothed,-1,kernel3)

cv2.imshow('Horizontal',s2)
cv2.imshow('Vertical',s)

cv2.waitKey(0)
cv2.destroyAllWindows()