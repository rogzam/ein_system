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

sec_on_mlt = 20
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
        
        while not wifi_ntw.isconnected():
            pass

    msg_tok = 'Token [ '+ tok_id + ' ] connected to IP: '+ str(wifi_ntw.ifconfig()[0])
    time.sleep(1)
    print(msg_tok)

def sec_on():
    
    sec_on_val = sec_on_mlt * sec_on_cyc
    for i in range(sec_on_cyc):
        for j in range(ring_pix):
            ring[j] = ((i+1)*sec_on_mlt,(i+1)*sec_on_mlt,(i+1)*sec_on_mlt)
            time.sleep_ms(30)
            ring.write()

    for i in range (sec_on_val):
        for j in range(ring_pix):
            dim = sec_on_val - i
            ring[j] = (dim,dim,dim)

        ring.write()
        time.sleep_ms(20)
    ring.fill((0,0,0))
    ring.write()
    
    msg_rdy = 'Token [ '+ tok_id + ' ] ready.'
    print(msg_rdy)

def send_msg():
    try:
        aio_client.publish(topic = aio_msgs, msg = 'Token [ '+ tok_id + ' ] connected to IP: '+ str(wifi_ntw.ifconfig()[0]))
        aio_client.publish(topic = aio_msgs, msg = 'Token [ '+ tok_id + ' ] ready.')
        print('Message published.')
    except Exception as e:
        print('Failed to publish message.')
    pass

def bat_val():
    aio_client.publish(topic = aio_msgs, msg = 'Battery = ' + str(bat.read()) + '/4100')
    print('Battery = ' + str(bat.read()) + '/4100')

## EXECUTION    

wifi_connect()
sec_on()
aio_client.connect()
send_msg()
bat_val()
