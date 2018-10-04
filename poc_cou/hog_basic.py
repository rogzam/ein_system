from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2
import argparse

parser = argparse.ArgumentParser(description='Process the defined image from the sample folder')
parser.add_argument('id', help='image number')
args = parser.parse_args()

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

image = cv2.imread('sample_photos/EIN_sample_{}.jpg'.format(str(args.id)))
#image = imutils.resize(image, width=min(400, image.shape[1]))

(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        padding=(8, 8), scale=1.05)

rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

cv2.imshow("HOG", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

