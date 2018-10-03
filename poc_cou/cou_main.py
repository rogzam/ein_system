### MAIN PUBLISHER FOR COUNTER LOOP / RZ - 2018 ##

## LIBRARIES

from Adafruit_IO import MQTTClient
import random
import time
import socket

## DEVICE ID

cou_id = '0001'

## DEFINITIONS

aio_key = '6d2080fc57374353ba8a59d11dcefbb3'
aio_user = 'rogzam'
aio_con = 'poc-ein.cou-con-'+ cou_id
aio_sts = 'poc-ein.cou-sts-'+ cou_id

aio_client = MQTTClient(aio_user, aio_key ,secure=False)

## FUNCTIONS 

def msg_rin(wait):
    '''Sends a random number to the feed'every X seconds'''

    while True:
        ran = random.randint(0,5)
        msg_con = 'COUNTER [{}] IS {}.'.format(cou_id,ran)
        msg_sts = ran
        print(msg_con)
        aio_client.publish(aio_con, msg_con)
        aio_client.publish(aio_sts, msg_sts)
        time.sleep(wait)

def msg_con():
    '''Sends connection status to the cloud console.'''

    cou_ip = socket.gethostbyname(socket.gethostname())
    
    try:       
        msg_con = 'COUNTER [{}] CONNECTED TO {}'.format(cou_id,cou_ip)
        aio_client.publish(aio_con, msg_con)
        print(msg_con)
    except Exception as e:
        pass
        print('FAILED TO PUBLISH COUNTER INITIAL CONNECTION')         

## EXECUTION

aio_client.connect()
aio_client.loop_background()
msg_con()
msg_rin(5)
