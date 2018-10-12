#Import the neccesary libraries
import numpy as np
import argparse
import cv2 

par = argparse.ArgumentParser(description='Script to run MobileNet-SSD object detection network')

par.add_argument("--image", default= "pho_sam/EIN_sample_01.jpg", help="path to video file. If empty, camera's stream will be used")
par.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",help='Path to text network file: ''MobileNetSSD_deploy.prototxt for Caffe model')
par.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",help='Path to weights: ''MobileNetSSD_deploy.caffemodel for Caffe model')
par.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")

par_arg = par.parse_args()

classNames = {15: 'person'}

ssd_net = cv2.dnn.readNetFromCaffe(par_arg.prototxt, par_arg.weights)

vid_cap = cv2.VideoCapture(0)

cou_pep = 0

while True:

    _, img_raw = vid_cap.read()

    img_rsz = cv2.resize(img_raw,(300,300)) 
    img_hfc = img_raw.shape[0]/300.0 #Height factor
    img_wfc = img_raw.shape[1]/300.0 #Width factor

    ssd_blb = cv2.dnn.blobFromImage(img_rsz, 0.007843, (300, 300), (127.5, 127.5, 127.5), False) #blob

    ssd_net.setInput(ssd_blb)
    ssd_det = ssd_net.forward() #detections()

    img_cop = img_raw.copy()
    img_col = img_rsz.shape[1] 
    img_row = img_rsz.shape[0]

    cv2.addWeighted(img_cop, 0.3, img_raw, 1 - 0.3, 0, img_raw) #0.3 is the opacity!?

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
    cou_pep = 0 
    cv2.namedWindow("SSD", cv2.WINDOW_NORMAL)
    cv2.imshow("", img_raw)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
