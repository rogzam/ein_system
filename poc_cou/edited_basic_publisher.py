### MAIN PUBLISHER FOR COUNTER LOOP / RZ - 2018 ##

## LIBRARIES

from Adafruit_IO import MQTTClient
import random
import time
import socket

## DEFINITIONS

aio_key = '6d2080fc57374353ba8a59d11dcefbb3'
aio_user = 'rogzam'
aio_con = 'poc-ein.con'

cou_id = 'A'

aio_client = MQTTClient(aio_user, aio_key ,secure=False)

## FUNCTIONS 

def msg_rin(wait):
    '''Sends a random number to the feed'every X seconds'''

    while True:
        msg = 'COUNTER [{}] IS {}.'.format(cou_id,random.randint(0, 5))
        print(msg)
        aio_client.publish(aio_con, msg)
        time.sleep(wait)

def msg_con():
    '''Sends connection status to the cloud console.'''

    cou_ip = socket.gethostbyname(socket.gethostname())
    
    try:       
        msg = 'COUNTER [{}] CONNECTED TO {}'.format(cou_id,cou_ip)
        aio_client.publish(aio_con, msg)
        print(msg)
    except Exception as e:
        pass
        print('FAILED TO PUBLISH COUNTER INITIAL CONNECTION')         

## EXECUTION

aio_client.connect()
aio_client.loop_background()
msg_con()
msg_rin(2)
