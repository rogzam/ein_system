### BASIC HOG PEOPLE COUNTER / RZ - 2018 ###

## LIBRARIES

from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2
import argparse

## PARSER

parser = argparse.ArgumentParser(description='Process the defined image from the sample folder')
parser.add_argument('-i','--id', default='01', help='image number')
args = parser.parse_args()

## DEFINITIONS

hog_des = cv2.HOGDescriptor()
hog_des.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

img_nam = 'sample_photos/EIN_sample_{}.jpg'.format(str(args.id))

img_raw = cv2.imread(img_nam)

## EXECUTION

(rects, weights) = hog_des.detectMultiScale(img_raw, winStride=(4, 4), padding=(8, 8), scale=1.05)

rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

for (xA, yA, xB, yB) in pick:
        cv2.rectangle(img_raw, (xA, yA), (xB, yB), (0, 255, 0), 2)

print("{} PEDESTRIANS DETECTED IN IMAGE '{}'.".format(len(rects),img_nam))
cv2.imshow("HOG", img_raw)
cv2.waitKey(0)
cv2.destroyAllWindows()

