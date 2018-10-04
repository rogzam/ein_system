### BASIC HOG PEOPLE COUNTER / RZ - 2018 ###

## LIBRARIES

from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2
import argparse
import datetime

## DEVICE ID

cou_id = '0001'


## PARSER

parser = argparse.ArgumentParser(description='Process the defined image from the sample folder')
parser.add_argument('-i','--id', default='01', help='image number')
args = parser.parse_args()

## DEFINITIONS

tim_now = datetime.datetime.now().strftime("%Y%m%d_%H%M")

hog_des = cv2.HOGDescriptor()
hog_des.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

img_nam = 'pho_sam/EIN_sample_{}.jpg'.format(str(args.id))

img_raw = cv2.imread(img_nam)
height, width = img_raw.shape[:2]

img_gry = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)

img_rzs = img_raw
#img_rzs = cv2.resize(img_raw,(int(width/2),int(height/2)))

## EXECUTION

(rects, weights) = hog_des.detectMultiScale(img_rzs, winStride=(4, 4), padding=(8, 8), scale=1.05)

rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

for (xA, yA, xB, yB) in pick:
        cv2.rectangle(img_rzs, (xA, yA), (xB, yB), (0, 255, 0), 2)

print("{} PEDESTRIANS DETECTED IN IMAGE '{}'.".format(len(rects),img_nam))
cv2.imshow("hog_basic", img_rzs)
cv2.imwrite('pho_pro/{}_[{}].png'.format(tim_now,cou_id),img_rzs)
cv2.waitKey(0)
cv2.destroyAllWindows()

