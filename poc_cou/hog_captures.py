### CAPTURER AND HOG COUNTER / RZ - 2018 ###

## LIBRARIES

from imutils.object_detection import non_max_suppression
import numpy as np
import cv2
import datetime
import time

## DEVICE ID

cou_id = '0001'

## DEFINITIONS

foo_src = 'foo_sam/foo_sam_01.MOV'
img_des = 'pho_pro/'

cap_fmt = '.png'
cyc_int = 200
cyc_cnt = 0

rsz_fct = 3

hog_des = cv2.HOGDescriptor()
hog_des.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

## FUNCTIONS

def rsz_img(img,fct):   
    '''Resizes an image by the factor indicated in both width and height'''
        
    h, w = img.shape[:2]
    img_rsz = cv2.resize(img,(int(w/fct),int(h/fct)))
    return img_rsz

def src_id(src):
    '''Takes the video source and assigns a string name in case the footage
       comes from the webcam directory'''
    
    if type(src) == int:
        src = 'CAMERA {}'.format(str(src))
        return src
    else:
        return src

def hog_img(src):
    '''Takes an image detects and counts full-body shapes. Returns both the image and
       an integer with the number of pedestrians counted.'''
    
    (rects, weights) = hog_des.detectMultiScale(src, winStride=(4, 4), padding=(8, 8), scale=1.05)

    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(src, (xA, yA), (xB, yB), (0, 0, 200), 2)

    cnt = len(rects)

    print("{} PEDESTRIANS DETECTED IN IMAGE '{}'.".format(cnt,img_nam))
    
    return src, cnt

def nam_img(fmt='.png'):
    '''Produces a name for the capture based on a timestamp and an image format defined above'''
    
    tim_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nam = '{}_[{}]{}'.format(tim_now,cou_id,fmt)
    return nam
    
## EXECUTION

vid_cap = cv2.VideoCapture(foo_src);

while True:

    _, img_raw = vid_cap.read()

    if cyc_cnt % cyc_int == 0:
               
        img_rsz = rsz_img(img_raw,rsz_fct)
        img_nam = nam_img(cap_fmt)
        img_hog, cnt_hog = hog_img(img_rsz)

        cv2.imwrite(img_des+img_nam, img_rsz)
        
        print('IMAGE CAPTURED FROM {} AND RESIZED BY {}.'.format(foo_src,rsz_fct))

    else:
        pass
    #print('EMPTY CYCLE')

    cyc_cnt+=1
    
