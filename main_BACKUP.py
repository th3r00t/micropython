import machine, esp, network, time
from ntptime import settime
from machine import UART
global rtc, nettime, serial_rx, serial_tx, uart, rx_data, sprint
rx_data = []
wlan=network.WLAN(network.STA_IF)
CON=False
wlan.active(1)

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

def serial_init():
    global uart
    uart = UART(1, 115200)
    uart.init(115200, bits=8, parity=None, stop=2)

def serial_rx():
    global uart, rx_data
    while not uart.any():
        time.sleep(1)
    buf = []
    uart.readinto(buf)
    rx_data = rx_data + buf

def serial_tx():
    global uart, rx_data
    # sprint("This is my first string of test data, it should split lines.")
    uart_test(1)

def rtc():
    now = machine.RTC()
    return now.datetime()

def nettime():
    clock = rtc()
    time = str(clock[4]-4)+':'+str(clock[5])+'.'+str(clock[6])
    return time

def uart_test(data):
    uart.write(data)

def sprint(data):
    data_len = len(data)
    if data_len > 20 & data_len < 80:
        uart.write(data)
    else:
        char_len = 20
        char_buf = [data[i:i+char_len] for i in range(0, len(data), char_len)]
        for line in char_buf:
            uart.write(line, "\r\n")

netconnect()
settime()  # Set rtc to ntptime
serial_init()
