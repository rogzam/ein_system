### CAPTURER AND SSD COUNTER / RZ - 2018 ###

## LIBRARIES

from Adafruit_IO import MQTTClient
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
import random
import numpy as np
import cv2
import datetime
import time
import socket
import base64
import argparse

## PARSER

par = argparse.ArgumentParser(description='Script to run MobileNet-SSD object detection network')

par.add_argument('-c','--cyc_int', default= 200, help="Program cycles before capture, default 200 for rpi, on mbp use 300 max.")
par.add_argument('-r','--rsz_fct', default= 1.4, help="Resize factor, increase in case image is to big for cloud.")
par.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",help='Path to text network file: ''MobileNetSSD_deploy.prototxt for Caffe model')
par.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",help='Path to weights: ''MobileNetSSD_deploy.caffemodel for Caffe model')
par.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")

par_arg = par.parse_args()

## DEVICE ID

cou_id = '0001'

## DEFINITIONS

aio_key = '6d2080fc57374353ba8a59d11dcefbb3'
aio_user = 'rogzam'
aio_con = 'poc-ein.cou-con-'+ cou_id
aio_sts = 'poc-ein.cou-sts-'+ cou_id
aio_img = 'poc-ein.cou-img-'+ cou_id

aio_client = MQTTClient(aio_user, aio_key ,secure=False)

camera = PiCamera()

rsz_fct = par_arg.rsz_fct
img_des = 'pho_pro/'

cap_fmt = '.jpeg'
cyc_int = par_arg.cyc_int
cyc_cnt = 0

classNames = {15: 'person'}

## FUNCTIONS

def rsz_img(img,fct):   
    '''Resizes an image by the factor indicated in both width and height'''

    #print(
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

def ssd_img(src):

    cou_pep = 0
    
    img_rsz = cv2.resize(img_raw,(300,300)) 
    img_hfc = img_raw.shape[0]/300.0 #Height factor
    img_wfc = img_raw.shape[1]/300.0 #Width factor

    ssd_blb = cv2.dnn.blobFromImage(img_rsz, 0.007843, (300, 300), (127.5, 127.5, 127.5), False) #blob

    ssd_net.setInput(ssd_blb)
    ssd_det = ssd_net.forward() #detections()

    img_col = img_rsz.shape[1] 
    img_row = img_rsz.shape[0]

    #cv2.addWeighted(img_cop, 0.3, img_raw, 1 - 0.3, 0, img_raw) #0.3 is the opacity!?

    for i in range(ssd_det.shape[2]):
        ssd_con = ssd_det[0, 0, i, 2] #Confidence of prediction 
        if ssd_con > par_arg.thr: # Filter prediction 
            class_id = int(ssd_det[0, 0, i, 1]) # Class label

            if class_id == 15:
                cou_pep = cou_pep+1
                
                img_xlt = int(ssd_det[0, 0, i, 3] * img_col) 
                img_ylt = int(ssd_det[0, 0, i, 4] * img_row)
                img_xrb = int(ssd_det[0, 0, i, 5] * img_col)
                img_yrb = int(ssd_det[0, 0, i, 6] * img_row)

                img_XLT = int(img_wfc * img_xlt) 
                img_YLT = int(img_hfc * img_ylt)
                img_XRB = int(img_wfc * img_xrb)
                img_YRB = int(img_hfc *img_yrb)
                
                cv2.rectangle(img_raw, (img_XLT, img_YLT), (img_XRB, img_YRB),(255,144,30),2)

                img_wid = img_XRB - img_XLT
                img_hei = img_YRB - img_YLT

                if class_id in classNames:
                    img_lab = str(ssd_con)

                    lab_size, baseLine = cv2.getTextSize(img_lab, cv2.FONT_HERSHEY_TRIPLEX, .75, 1)

                    img_YRB = max(img_YRB, lab_size[1])

                    cv2.rectangle(img_raw,(img_XLT,img_YLT+img_hei),(img_XLT+lab_size[0],img_YLT+img_hei-lab_size[1]),(255,144,30), cv2.FILLED)
                    cv2.putText(img_raw, img_lab, (img_XLT, img_YLT+img_hei),cv2.FONT_HERSHEY_TRIPLEX, .75, (255, 255, 255))

    if cou_pep > 0:
        cv2.putText(img_raw,'{} PEDESTRIANS DETECTED'.format(str(cou_pep)),(int(img_raw.shape[1]/30),int(img_raw.shape[0] - img_raw.shape[0]/20)),cv2.FONT_HERSHEY_TRIPLEX,.5,(255,255,255),1,cv2.LINE_AA);

    print('DETECTIONS = ' + str(cou_pep))

    return img_raw,cou_pep

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
    
    msg_sts = cou_pep
    msg_con = "COUNTER [{}] DETECTED {} PEDESTRIANS IN IMAGE {}.".format(cou_id,cou_pep,img_nam)

    print(msg_con)

    aio_client.publish(aio_con, msg_con)
    aio_client.publish(aio_sts, msg_sts)

def msg_img():
    '''Sends image information to cloude console'''

    rzs_ssd = rsz_img(ssd_cap,rsz_fct)

    cv2.imwrite(img_des+'LR_'+img_nam, rzs_ssd)

    img_opn = open(img_des+'LR_'+img_nam,'rb')
    str_img = base64.b64encode(img_opn.read())

    msg_con = "COUNTER [{}] SAVED NEW IMAGE ({}KBs) IN {} DIRECTORY.".format(cou_id,len(str_img),img_des)
        
    aio_client.publish(aio_con, msg_con)
    aio_client.publish(aio_img, str_img)

    print(msg_con)

## EXECUTIONi

aio_client.connect()
aio_client.loop_background()

msg_net()

ssd_net = cv2.dnn.readNetFromCaffe(par_arg.prototxt, par_arg.weights)

time.sleep(.5)

while True:
    
    img_nam = nam_img(cap_fmt)

    print(str(cyc_cnt))
    
    if cyc_cnt % cyc_int == 0:

        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture,format='bgr')
        img_pi = rawCapture.array
        img_raw = cv2.flip(img_pi,0)

        ssd_cap, cou_pep = ssd_img(img_raw)
               
        msg_cap()
        
        cv2.imwrite(img_des+img_nam, ssd_cap)
        
        msg_img()

        rawCapture.truncate(0)

    else:
        pass    
    
    cyc_cnt+=1
    
