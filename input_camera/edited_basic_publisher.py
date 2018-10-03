### MAIN PUBLISHER FOR CAMERA LOOP / RZ - 2018 ##

## LIBRARIES

from Adafruit_IO import MQTTClient
import random
import time

## DEFINITIONS

aio_key = '6d2080fc57374353ba8a59d11dcefbb3'
aio_user = 'rogzam'
aio_lin = 'ein-system.ter-lin'

aio_client = MQTTClient(aio_user, aio_key ,secure=False)

## FUNCTIONS 

def msg_rin(wait):

    while True:
        msg = random.randint(0, 5)
        print('Publishing {0}.'.format(msg))
        aio_client.publish(aio_lin, msg)
        time.sleep(wait)

## EXECUTION

aio_client.connect()
aio_client.loop_background()
msg_rin(2)
