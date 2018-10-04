import cv2
import time

vid_cap = cv2.VideoCapture('foo_sam/foo_sam_01.MOV');
#WEBCAM#vid_cap = cv2.VideoCapture(0);

count = 0

def rsz(image,fac=2):
    '''Resizes an image by the factor indicated in both width and height'''
    h, w = image.shape[:2]
    img_rsz = cv2.resize(image,(int(w/2),int(h/2)))
    return img_rsz

img_ini = rsz(vid_cap.read()[1],2)


while 1:
    img_raw = vid_cap.read()[1]
    print('read a new frame:')
    
    if count%5 == 0 :
        img_rsz = rsz(img_raw,2)        
        cv2.imwrite('frame%d.jpg'%count,img_raw)
        print('success')
        
    count+=1
    cv2.imshow('Holder', img_ini)
    time.sleep(1)
    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break

vid_cap.release()
cv2.destroyAllWindows()
