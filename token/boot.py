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

aio_server = 'io.adafruit.com'
aio_port = 1883
aio_user = 'rogzam'
aio_key = '6d2080fc57374353ba8a59d11dcefbb3'
aio_id = 'whatever_client_id'
aio_msgs = 'rogzam/feeds/msgs'
aio_client = MQTTClient(aio_id, aio_server, aio_port, aio_user, aio_key)

tok_id = '0001'

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

    msg_tok = 'TOKEN ['+tok_id+'] CONNECTED TO: '+ str(wifi_ntw.ifconfig()[0])
    print(msg_tok)

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
    
    msg_rdy = 'TOKEN ['+ tok_id +'] READY.'
    print(msg_rdy)

def send_msg():
    
    try:
        time.sleep(0.2)
        aio_client.publish(topic = aio_msgs, msg = 'TOKEN ['+tok_id+'] CONNECTED TO: '+ str(wifi_ntw.ifconfig()[0]))
        print('MESSAGE PUBLISHED.')
    except Exception as e:
        print('FAILED TO PUBLISH MESSAGE.')
    pass

def bat_lvl():

    lvl = bat.read()* 2 * 100 / 4700
    time.sleep(0.4)
    aio_client.publish(topic = aio_msgs, msg = 'BATTERY LEVEL: '+ str(lvl)+'%')
    print('BATTERY LEVEL: {:.2f} %'.format(lvl))

## EXECUTION    

wifi_connect()
sec_on()
aio_client.connect()
send_msg()
bat_lvl()
