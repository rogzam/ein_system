import cv2
import numpy as np

body_cascade = cv2.CascadeClassifier('lib_haar/haarcascade_fullbody.xml')

img = cv2.imread('pho_sam/EIN_sample_01.jpg',cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

bodies = body_cascade.detectMultiScale(gray, minNeighbors=1,scaleFactor=1.05,minSize = (80,80),maxSize=(150,300))

font = cv2.FONT_HERSHEY_SIMPLEX

for (x,y,w,h) in bodies:
    
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    roi_gray= gray[y:y+h,x:x+w]
    roi_color = img[y:y+h,x:x+w]

cv2.imshow('Haar',img)
#cv2.imshow('gray',gray)    

cv2.waitKey(0)
cv2.destroyAllWindows()

