### FACE DETECTION USING HAAR CASCADE DESCRIPTOR - INITIAL EXAMPLE - LEARNED HOW TO COUNT DETECTIONS

import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('lib_haar/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('lib_haar/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while 1:
    ret,img = cap.read()
    height, width = img.shape[:2]

    rimg = cv2.resize(img,(int(width/2),int(height/2)));
    
    gray = cv2.cvtColor(rimg, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(45,45),0)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 1:
        cv2.putText(rimg,('1 face detected.'),(int(width/2-630),int(height/2-8)), font,.5,(255,255,255),1,cv2.LINE_AA);
        
    elif len(faces) > 1:
        cv2.putText(rimg,(str(len(faces)) + ' faces detected.'),(int(width/2-630),int(height/2-8)), font,.5,(255,255,255),1,cv2.LINE_AA);
        
    else:
        cv2.putText(rimg,('No face detected.'),(int(width/2-630),int(height/2-8)), font,.5,(255,255,255),1,cv2.LINE_AA);

              
    for (x,y,w,h) in faces:
        
        cv2.imshow('rimg',blur,)
        cv2.rectangle(rimg,(x,y),(x+w,y+h),(0,0,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = rimg[y:y+h,x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        cv2.putText(rimg,('X: '+str(x)+' - '+'Y: '+str(y)),(x,y-10), font,.4,(255,255,255),1,cv2.LINE_AA)
        
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),1)
    

    cv2.imshow('rimg',rimg)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
