
### BOOT FILE FOR TOKEN INITIALIZATION / RZ - 2018 ###

import network
import machine
import neopixel
import time

## DEFINITIONS

ring_pix = 16
ring_pin = 22
ring = neopixel.NeoPixel(machine.Pin(ring_pin), ring_pix)

sec_on_mlt = 20
sec_on_cyc = 3

wifi_ssid = "Rog"
wifi_pass = "Roghotspot88"
wifi_ntw = network.WLAN(network.STA_IF)

tok_id = '0001'

## MESSAGES

msg_tok = 'Token [ '+ tok_id + ' ] connected to IP: '+ wifi_ntw.ifconfig()[0]
msg_rdy = 'Token [ '+ tok_id + ' ] ready.'

## FUNCTIONS

def wifi_connect():
    
    if not wifi_ntw.isconnected():
        wifi_ntw.active(True)
        wifi_ntw.connect(wifi_ssid,wifi_pass)
        while not wifi_ntw.isconnected():
            pass
        
    print(msg_tok)

def send_msg():
    pass

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
    
    print(msg_rdy)

## EXECUTION    

wifi_connect()
sec_on()
