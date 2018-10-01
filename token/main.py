### MAIN FILE FOR TOKEN LOOP / RZ - 2018 ###

## LIBRARIES

import neopixel
import machine
import network
import time
from umqtt.simple import MQTTClient

## DEFINITIONS

ring_pix = 16
ring_pin = 22
ring = neopixel.NeoPixel(machine.Pin(ring_pin), ring_pix)

bat = machine.ADC(machine.Pin(35))
bat.atten(3)

sec_on_mlt = 30
sec_on_cyc = 3

wifi_ssid = "Rog"
wifi_pass = "Roghotspot88"
wifi_ntw = network.WLAN(network.STA_IF)

tkn_id = '0001'

aio_server = 'io.adafruit.com'
aio_port = 1883
aio_user = 'rogzam'
aio_key = '6d2080fc57374353ba8a59d11dcefbb3'
aio_id = 'whatever_client_id'
aio_sts = 'rogzam/feeds/ein-system.tkn-{}-sts'.format(tkn_id)
aio_bat = 'rogzam/feeds/ein-system.tkn-{}-bat'.format(tkn_id)
aio_lin = 'rogzam/feeds/ein-system.ter-lin'
aio_client = MQTTClient(aio_id, aio_server, aio_port, aio_user, aio_key)

msg_dec = 0

## FUNCTIONS
        
def wifi_connect():
    
    if not wifi_ntw.isconnected():
        wifi_ntw.active(True)
        wifi_ntw.connect(wifi_ssid,wifi_pass)
        
        for i in range(3):
            while not wifi_ntw.isconnected():
                print('CONNECTION ATTEMPT: '+str(i+1)+ '...')
                time.sleep(0.4)
                pass

def sub_cb(topic,msg):
    
    global msg_dec
    
    msg_dec = int(msg.decode('UTF-8'))
    
    return msg_dec

def tkn_sec(msg_dec,speed=8):

    if msg_dec == 1: 
        for i in range(0,2*512,speed):
            for j in range (ring_pix):
                if (i // 256) % 2 == 0:
                    val = i
                else:
                    val = 255 - i    
                ring[j] = (0,val,0)
            ring.write()
            time.sleep_ms(30)

    elif msg_dec == 2: 
        for i in range(0,2*512,speed):
            for j in range (ring_pix):
                if (i // 256) % 2 == 0:
                    val = i
                else:
                    val = 255 - i    
                ring[j] = (val,val,0)   
            ring.write()
            time.sleep_ms(30)
            
    elif msg_dec == 3:    
        for i in range(0,2*512,speed):
            for j in range (ring_pix):
                if (i // 256) % 2 == 0:
                    val = i
                else:
                    val = 255 - i    
                ring[j] = (val,0,0)
            ring.write()
            time.sleep_ms(30)        

    else: 
        for i in range(0,1*512,speed):
            for j in range (ring_pix):
                if (i // 256) % 2 == 0:
                    val = i
                else:
                    val = 255 - i    
                ring[j] = (val,val,val)
            ring.write()
            time.sleep_ms(30)

    for i in range(3):        
        ring.fill((0,0,0))
        ring.write()

    time.sleep(4)

def tkn_loop():

    while True:
        aio_client.check_msg()
        tkn_sec(msg_dec)

wifi_connect()
aio_client.set_callback(sub_cb)
aio_client.connect()
aio_client.subscribe(aio_lin)

tkn_loop()
