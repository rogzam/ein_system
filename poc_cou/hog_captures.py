### BASIC HOG PEOPLE COUNTER / RZ - 2018 ###

## LIBRARIES

from imutils.object_detection import non_max_suppression
import numpy as np
import cv2
import datetime
import time

## CAPTURE IMAGE

vid_cap = cv2.VideoCapture('foo_sam/foo_sam_01.MOV');

count = 0

def rsz(image,fac=2):
    '''Resizes an image by the factor indicated in both width and height'''
    h, w = image.shape[:2]
    img_rsz = cv2.resize(image,(int(w/2),int(h/2)))
    return img_rsz

img_ini = rsz(vid_cap.read()[1],2)

img_a = vid_cap.read()[1]
print('read a new frame:')

img_rsz = rsz(img_a,2)

cv2.imwrite('pho_sam/frame.jpg',img_a)
print('success')

count+=1
cv2.imshow('Holder', img_ini)

vid_cap.release()

## IMAGE ANALIZED

## DEVICE ID

cou_id = '0001'

## DEFINITIONS

tim_now = datetime.datetime.now().strftime("%Y%m%d_%H%M")

hog_des = cv2.HOGDescriptor()
hog_des.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

img_nam = 'pho_sam/frame.jpg'

img_raw = cv2.imread(img_nam)
height, width = img_raw.shape[:2]

img_gry = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)

img_rsz = img_raw
#img_rsz = cv2.resize(img_raw,(int(width/2),int(height/2)))

## EXECUTION

(rects, weights) = hog_des.detectMultiScale(img_rsz, winStride=(4, 4), padding=(8, 8), scale=1.05)

rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

for (xA, yA, xB, yB) in pick:
        cv2.rectangle(img_rsz, (xA, yA), (xB, yB), (0, 0, 200), 2)

print("{} PEDESTRIANS DETECTED IN IMAGE '{}'.".format(len(rects),img_nam))
cv2.imshow("hog_basic", img_rsz)
cv2.imwrite('pho_pro/{}_[{}].png'.format(tim_now,cou_id),img_rsz)
cv2.waitKey(0)
cv2.destroyAllWindows()

