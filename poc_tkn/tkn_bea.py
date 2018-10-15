## LIBRARIES

import neopixel
import machine
import network
import time

## DEFINITIONS

ring_pix = 12
ring_pin = 22
ring = neopixel.NeoPixel(machine.Pin(ring_pin), ring_pix)

## EXECUTION

def tkn_bea(bea_cyc,bea_spe,bea_col,bea_sle,bea_div,bea_act):
    '''Generates beat pattern defined by the cycles per beat, the speed of the beat,
       the color of the beat and the amounts of seconds between beats'''

    global pix_val
    
    for i in range(0,bea_cyc*512,bea_spe):
        for j in range ((ring_pix/bea_div)*(bea_act)):
            if (i // 256) % 2 == 0:
                pix_val = i
            else:
                pix_val = 255 - i            

## PROPER COLOR DICTIONARY, COMMENTED TO ADJUST AFTER RING SOLDERING FUCK-UP

##            col_dic = { 'whi' : (pix_val, pix_val, pix_val), 
##                        'yel' : (pix_val, pix_val, 0),
##                        'cya' : (0, pix_val, pix_val),
##                        'pur' : (pix_val, 0, pix_val),
##                        'red' : (pix_val, 0, 0),
##                        'gre' : (0, pix_val, 0),
##                        'blu' : (0, 0, pix_val), }
            
            col_dic = { 'whi' : (pix_val, pix_val, pix_val),
                        'yel' : (pix_val, pix_val, 0),
                        'pur' : (0, pix_val, pix_val),
                        'cya' : (pix_val, 0, pix_val),
                        'gre' : (pix_val, 0, 0),
                        'red' : (0, pix_val, 0),
                        'blu' : (0, 0, pix_val), }            

            ring[j] = col_dic[bea_col]

        ring.write()
        time.sleep(.02)

    for i in range(3):        
        ring.fill((0,0,0))
        ring.write()
        
    time.sleep(bea_sle)

while True:

    tkn_bea(3, 40, 'red', 1, 4, 3)    
