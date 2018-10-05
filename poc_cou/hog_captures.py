### CAPTURER AND HOG COUNTER / RZ - 2018 ###

## LIBRARIES

from Adafruit_IO import MQTTClient
from PIL import Image
import random
from imutils.object_detection import non_max_suppression
import numpy as np
import cv2
import datetime
import time
import socket
import base64

## DEVICE ID

cou_id = '0001'

## DEFINITIONS

aio_key = '6d2080fc57374353ba8a59d11dcefbb3'
aio_user = 'rogzam'
aio_con = 'poc-ein.cou-con-'+ cou_id
aio_sts = 'poc-ein.cou-sts-'+ cou_id
aio_img = 'poc-ein.cou-img-'+ cou_id

aio_client = MQTTClient(aio_user, aio_key ,secure=False)

foo_src = 'foo_sam/foo_sam_01.MOV'
img_des = 'pho_pro/'

cap_fmt = '.jpeg'
cyc_int = 1000
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
    
    return src, cnt

def nam_img(fmt='.png'):
    '''Produces a name for the capture based on a timestamp and an image format defined above'''
    
    tim_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nam = '{}_[{}]{}'.format(tim_now,cou_id,fmt)
    return nam

def msg_net():
    '''Sends connection status to the cloud console.'''

    cou_ip = socket.gethostbyname(socket.gethostname())
    
    try:       
        msg_net = 'COUNTER [{}] CONNECTED TO {}'.format(cou_id,cou_ip)
        aio_client.publish(aio_con, msg_net)
        print(msg_net)
        
    except Exception as e:
        pass
        print('FAILED TO PUBLISH COUNTER [{}] INITIAL CONNECTION'.format(cou_id))

def msg_cap():
    '''Sends counter capture info to the cloud console'''
    
    msg_sts = cnt_hog
    msg_con = "COUNTER [{}] DETECTED {} PEDESTRIANS IN IMAGE {}.".format(cou_id,cnt_hog,img_nam)

    print(msg_con)

    aio_client.publish(aio_con, msg_con)
    aio_client.publish(aio_sts, msg_sts)

def msg_img():
    '''Sends image information to cloude console'''

    gry_hog = cv2.cvtColor(img_hog, cv2.COLOR_BGR2GRAY)
    rzs_hog = rsz_img(img_hog,1.3)

    cv2.imwrite(img_des+img_nam, rzs_hog)

    img_opn = open(img_des+img_nam,'rb')
    str_img = base64.b64encode(img_opn.read())

    msg_con = "COUNTER [{}] SAVED NEW IMAGE ({}KBs) IN {} DIRECTORY.".format(cou_id,len(str_img),img_des)
        
    aio_client.publish(aio_con, msg_con)
    aio_client.publish(aio_img, str_img)

    print(msg_con)

## EXECUTION

aio_client.connect()
aio_client.loop_background()
msg_net()
vid_cap = cv2.VideoCapture(foo_src);

while True:

    _, img_raw = vid_cap.read()                 

    if cyc_cnt % cyc_int == 0:
               
        img_rsz = rsz_img(img_raw,rsz_fct)  
        img_nam = nam_img(cap_fmt)
        
        img_hog, cnt_hog = hog_img(img_rsz)

        msg_cap()

        cv2.imwrite(img_des+img_nam, img_rsz)

        msg_img()

    else:
        pass
    #print('EMPTY CYCLE')

    cyc_cnt+=1
    
