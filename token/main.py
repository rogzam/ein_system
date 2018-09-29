import random as ran
import time                               
from umqtt.simple import MQTTClient       
import machine                            
import neopixel

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "rogzam"
AIO_KEY = "6d2080fc57374353ba8a59d11dcefbb3"
AIO_CLIENT_ID = 'whateverthafuck'
AIO_CONTROL_FEED = "rogzam/feeds/lights"
AIO_RANDOMS_FEED = "rogzam/feeds/randoms"

# SETUP NEOPIXELS

pix_n = 16
pin_in = 22
np = neopixel.NeoPixel(machine.Pin(pin_in), pix_n)

print("Connected to Wifi")

# FUNCTIONS

def sub_cb(topic, msg):          # sub_cb means "callback subroutine"
    if msg == b"0":             # If message says "ON" ...
        np.fill((0,255,0))       # ... then LED on
        np.write()
        time.sleep(1)
    elif msg == b"1":          # If message says "OFF" ...
        np.fill((0,0,0))         # ... then LED off
        np.write()
        time.sleep(1)
    else:                        # If any other message is received ...
        print("Unknown message") # ... do nothing but output that it happened.

def random_integer(upper_bound):
    return ran.randint(1,5000) % upper_bound

def send_random():
    some_number = random_integer(100)
    print("Publishing: {0} to {1} ... ".format(some_number, AIO_RANDOMS_FEED), end='')
    time.sleep(5)
    try:
        client.publish(topic=AIO_RANDOMS_FEED, msg=str(some_number))
        print("DONE")
    except Exception as e:
        print("FAILED")

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

# Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
client.subscribe(AIO_CONTROL_FEED)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_CONTROL_FEED))

while True:             
    client.check_msg()# Action a message if one is received. Non-blocking.
    send_random()     # Send a random number to Adafruit IO if it's time.
    print('Message sent.')

