## BOOT FILE FOR TOKEN INITIALIZATION

import network
import machine
import neopixel
import time

## SET-UP 

pix_n = 16
pin_in = 22

wifi_ssid = "TSHGuest"
wifi_pass = ""

np = neopixel.NeoPixel(machine.Pin(pin_in), pix_n)

time.sleep(1)
np.fill((0,0,0))
np.write()

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('...connecting...')
    sta_if.active(True)
    sta_if.connect(wifi_ssid,wifi_pass)
    while not sta_if.isconnected():
        pass
    
print('CONNECTED', sta_if.ifconfig())

mlt = 20
cyc = 4
val_on = mlt * cyc

while True:
    
    for i in range(cyc):
        for j in range(pix_n):
            np[j] = ((i+1)*mlt,(i+1)*mlt,(i+1)*mlt)
            time.sleep_ms(30)
            np.write()

    for i in range (val_on):
        for j in range(pix_n):
            dim = val_on - i
            np[j] = (dim,dim,dim)

        np.write()
        time.sleep_ms(20)

    np.fill((0,0,0))
    np.write()

    break    

print('DEVICE READY')
