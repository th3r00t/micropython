import machine, esp, network, time, micropython
from ntptime import settime
from umqttsimple import MQTTClient
import ubinascii

global rtc, nettime, toggle, LIGHT, CON
rx_data = []
wlan=network.WLAN(network.STA_IF)
CON=False
wlan.active(1)
LIGHT=0

def netconnect():
    # Connect to local wireless network
    global CON
    try:
        while not CON:
            wlan.connect('WvItGuyMobile', 'A!ec4597778')
            if wlan.isconnected():
                CON=True
            else:
                pass
    except:
        if wlan.isconnected():
            print("Already Connected")
        else:
            print("Error Connecting")

def rtc():
    now = machine.RTC()
    return now.datetime()

def nettime():
    clock = rtc()
    time = str(clock[4]-4)+':'+str(clock[5])+'.'+str(clock[6])
    return time

def toggle(**kwargs):
    global LIGHT
    light = machine.Pin(3, machine.Pin.OUT)
    if LIGHT == 0:
        light.value(1)
        LIGHT = 1
    else:
        light.value(0)
        LIGHT = 0

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'home/lab/benchlight'
topic_pub = b'home/lab/benchlight/status'
message_interval = 5
last_message = 0
mqtt_server = '192.168.43.200'
toggle()
time.sleep(2)
netconnect()

def sub_cb(topic, msg):
    if topic == b'home/lab/benchlight' and msg == b'toggle':
        toggle()

def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server, user='home', password='A@2cb13')
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    return client

def restart_and_connect():
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_connect()

while True:
    try:
        client.check_msg()
        time.sleep(1)
    except OSError as e:
        restart_and_connect()
