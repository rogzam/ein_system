### BOOT FILE FOR TOKEN INITIALIZATION / RZ - 2018 ###

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
aio_client = MQTTClient(aio_id, aio_server, aio_port, aio_user, aio_key)


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

def sec_on():
    
    sec_on_val = sec_on_mlt * sec_on_cyc
    for i in range(sec_on_cyc):
        for j in range(ring_pix):
            ring[j] = ((i+1)*sec_on_mlt,(i+1)*sec_on_mlt,(i+1)*sec_on_mlt)
            time.sleep(0.05)
            ring.write()

    time.sleep(0.4)

    for i in range (sec_on_val):
        for j in range(ring_pix):
            dim = sec_on_val - i
            ring[j] = (dim,dim,dim)
        ring.write()
        time.sleep(0.02)
        
    ring.fill((0,0,0))
    ring.write()

def msg_sts():
    try:
        time.sleep(0.4)
        aio_client.publish(topic = aio_sts, msg = 'TOKEN ['+tkn_id+'] CONNECTED TO: '+ str(wifi_ntw.ifconfig()[0]))
        print('TOKEN ['+tkn_id+'] CONNECTED TO: '+ str(wifi_ntw.ifconfig()[0]))
        print('STATUS PUBLISHED.')
    except Exception as e:
        print('FAILED TO PUBLISH STATUS.')
    pass

def msg_bat():
    lvl = bat.read()* 2 * 100 / 4700
    try:       
        time.sleep(0.4)
        aio_client.publish(topic = aio_sts, msg = 'BATTERY LEVEL: {:.2f} %'.format(lvl))
        time.sleep(0.4)
        aio_client.publish(topic = aio_bat, msg = str(bat.read()*2))
        print('BATTERY LEVEL: {:.2f} %'.format(lvl))
        print('BATTERY LEVEL PUBLISHED.')
    except Exeption as e:
        print('FAILED TO PUBLISH BATTERY LEVEL.')
    pass    

## EXECUTION    

wifi_connect()
aio_client.connect()
sec_on()
msg_sts()
msg_bat()
