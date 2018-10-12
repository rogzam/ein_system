from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


while 1:
    ret,image = cap.read()

    height, width = image.shape[:2]

    rimg = cv2.resize(image,(int(width/2),int(height/2)));
    
    gray = cv2.cvtColor(rimg, cv2.COLOR_BGR2GRAY)
    
    (rects, weights) = hog.detectMultiScale(gray, winStride=(4, 4),
        padding=(8, 8), scale=1.05)

    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    for (xA, yA, xB, yB) in rects:
        cv2.rectangle(rimg, (xA, yA), (xB, yB), (0, 255, 0), 2)

    cv2.imshow('HOG',rimg)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
