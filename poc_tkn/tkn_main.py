### MAIN FILE FOR TOKEN LOOP / RZ - 2018 ###

## LIBRARIES

from umqtt.simple import MQTTClient
import neopixel
import machine
import network
import time

## DEVICE ID 

tkn_id = '0001'

## DEFINITIONS

ring_pix = 16
ring_pin = 22
ring = neopixel.NeoPixel(machine.Pin(ring_pin), ring_pix)

bat = machine.ADC(machine.Pin(35))
bat.atten(3)

onb_led = machine.Pin(13,machine.Pin.OUT)
usb_pin = machine.Pin(12,machine.Pin.IN)

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
aio_con = 'rogzam/feeds/poc-ein.tkn-con-'+ tkn_id
aio_sts = 'rogzam/feeds/poc-ein.tkn-sts-'+ tkn_id
aio_bat = 'rogzam/feeds/poc-ein.tkn-bat-'+ tkn_id

cou_sim = 'rogzam/feeds/poc-ein.cou-sim'


##aio_con = 'rogzam/feeds/poc-ein.con'
##aio_bat = 'rogzam/feeds/poc-ein.tkn-{}-bat'.format(tkn_id)
aio_client = MQTTClient(aio_id, aio_server, aio_port, aio_user, aio_key)

msg_dec = 0

col_dic = { 0 : 'WHITE',
            1 : 'GREEN',
            2 : 'YELLOW',
            3 : 'RED',
            4 : 'BLUE',
            5 : 'PURPLE', }

## FUNCTIONS

def onb_bli():
    '''Blinks the on-board led'''

    onb_led.value(1)
    time.sleep(.1)
    onb_led.value(0)
        
def wifi_connect():
    '''Connects to network using ssid & passwords introduced at the definition section.
       Also tries to connect to wifi 20 times, after that, it goes into deepsleep mode.'''

    cnt = 0
    
    if not wifi_ntw.isconnected():
        wifi_ntw.active(True)
        wifi_ntw.connect(wifi_ssid,wifi_pass)
        
        while not wifi_ntw.isconnected():
            print('CONNECTION ATTEMPT {}...'.format(str(cnt)))
            time.sleep(0.5)

            if cnt >= 27:
                cnt = 0
                print('TOKEN [{}] GOING INTO DEEP SLEEP MODE.'.format(tkn_id))
                machine.deepsleep()      
            else:
                cnt = cnt + 1
                pass            
    
##def sec_chr():
##    '''Draws a charging secuence on the LED ring, starts with an incremental spiral that
##       multiplies its brightness on every cycle. Then dims down to zero'''
##
##    ring.fill((0,0,20))
##    ring.write()
##    time.sleep(1)
##
##        sec_on_val = sec_on_mlt * sec_on_cyc
##        for i in range(sec_on_cyc):
##            for j in range(ring_pix):
##                ring[j] = (0,0,(i+1)*sec_on_mlt)
##                time.sleep(0.05)
##                ring.write()
##
##        for i in range (sec_on_val):
##            for j in range(ring_pix):
##                dim = sec_on_val - i
##                ring[j] = (dim,dim,dim)
##            ring.write()
##            time.sleep(0.02)
##            
##        tkn_cle()

def sec_on():
    '''Draws an on secuence on the LED ring, starts with an incremental spiral that
       multiplies its brightness on every cycle. Then dims down to zero'''
    
    print('TOKEN [{}] ON SECUENCE'.format(tkn_id))
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
        
    tkn_cle()
    time.sleep(.5)

def msg_con():
    '''Sends a string connection message to the cloud console'''
    
    try:
        msg_con = 'TOKEN ['+tkn_id+'] CONNECTED TO: '+ str(wifi_ntw.ifconfig()[0])
        aio_client.publish(topic=aio_con, msg=msg_con)
        print(msg_con)
    except Exception as e:
        print('FAILED TO PUBLISH TOKEN [{}] INITIAL CONNECTION STATUS.'.format(tkn_id))
        pass

def msg_bat():
    '''Sends a battery level message to the cloud broker both as a percentage string and as an raw int.
       To avoid lipo misreadings, if the reading is above 4.7 the battery it is then charged 100%'''

    bat_lvl = bat.read()*2
    
    if bat_lvl >= 4700:
        bat_con = 4700
    else:
        bat_con = bat_lvl
    
    bat_per = bat_con*100 / 4700
    
    try:       
        msg_bat = str(bat.read()*2)
        msg_con = 'TOKEN [{}] BATTERY LEVEL IS {:.2f} %'.format(tkn_id,bat_per)
        aio_client.publish(topic=aio_bat, msg=msg_bat)
        aio_client.publish(topic=aio_con, msg=msg_con )
        print(msg_con)
    except Exception as e:
        pass
        print('FAILED TO PUBLISH BATTERY LEVEL.')

def msg_sts(bea_cyc,bea_sle):
    '''Sends a token status to the cloud broker. Include description of the beat.'''
    
    try:       
        msg_sts = str(msg_dec)
        msg_con = 'TOKEN [{}] IS {}, WITH {} BEATS EVERY {} SECONDS.'.format(tkn_id,col_dic[msg_dec],str(bea_cyc),str(bea_sle))
        aio_client.publish(topic=aio_sts, msg=msg_sts)
        aio_client.publish(topic=aio_con, msg=msg_con)
        print(msg_con)
    except Exception as e:
        pass
        print('FAILED TO PUBLISH TOKEN STATUS') 

def sub_cb(topic,msg):
    '''Catches message from cloud broker and decodes it into a variable'''
    
    global msg_dec
    
    msg_dec = int(msg.decode('UTF-8'))
    
    return msg_dec

def tkn_bea(bea_cyc=2,bea_spe=4,bea_col='whi',bea_sle=5):
    '''Generates beat pattern defined by the cycles per beat, the speed of the beat,
       the color of the beat and the amounts of seconds between beats'''

    msg_sts(bea_cyc,bea_sle)

    for i in range(0,bea_cyc*512,bea_spe):
        for j in range (ring_pix):
            if (i // 256) % 2 == 0:
                val = i
            else:
                val = 255 - i

            if bea_col == 'whi':
                ring[j] = (val,val,val)
            elif bea_col == 'gre':
                ring[j] = (0,val,0)
            elif bea_col == 'yel':
                ring[j] = (val,val,0)
            elif bea_col == 'red':
                ring[j] = (val,0,0)
            elif bea_col == 'blu':
                ring[j] = (0,0,val)
            else:
                bea_col == 'pur'
                ring[j] = (val,0,val)

        ring.write()
        time.sleep(.02)

    tkn_cle()
    time.sleep(bea_sle)

def tkn_sec():
    '''Gets the decoded message and translates it into a beating secuence'''
    
    if msg_dec == 0:        
        tkn_bea(bea_cyc=2,bea_spe=4,bea_col='whi',bea_sle=5)
        
    elif msg_dec == 1:      
        tkn_bea(bea_cyc=2,bea_spe=4,bea_col='gre',bea_sle=5)

    elif msg_dec == 2:      
        tkn_bea(bea_cyc=2,bea_spe=4,bea_col='yel',bea_sle=2)

    elif msg_dec == 3:      
        tkn_bea(bea_cyc=2,bea_spe=4,bea_col='red',bea_sle=0)

    elif msg_dec == 4:      
        tkn_bea(bea_cyc=2,bea_spe=4,bea_col='blu',bea_sle=5)    

    else:
        tkn_bea(bea_cyc=2,bea_spe=4,bea_col='pur',bea_sle=1)
        
def tkn_cle():
    '''Cleans the emissions from the ring'''
    
    for i in range(3):        
        ring.fill((0,0,0))
        ring.write()

def tkn_loop():
    '''Loops constantly through the message callback and the beating sequence,
       sending a battery message status every four itterations'''

    sec_cou = 0
    while True:

        aio_client.check_msg()
        tkn_sec()

        if sec_cou == 4:
            msg_bat()
            sec_cou = 0
        else:
            sec_cou = sec_cou +1


##def usb_chk():
##    usb_sts = 0
##    
##    for i in range(3):
##        usb_sts = usb_sts + usb_pin.value()
##        time.sleep(.02)
##        
##    return usb_sts    
    
            
## EXECUTION        

onb_bli()

tkn_cle()
wifi_connect()
aio_client.set_callback(sub_cb)
aio_client.connect()
aio_client.subscribe(cou_sim)
msg_con()
sec_on()

tkn_loop()

