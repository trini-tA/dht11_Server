from machine import Pin, I2C
import ssd1306

import utime as time
from screen import Screen
from server import Server
from dht11 import DHT11
from ifconfig import IFCONFIG
import socket
import json

VERSION = "0.1"
NAME = "TSRV"
DISPLAY_NAME = NAME + " " + VERSION
PIN_TEMP = 2                # on board -> D4

#screen
PIN_OLED_SCL = 5            # on board -> D1
PIN_OLED_SDA = 4            # on board -> D2

# using default address 0x3C
i2c = I2C(sda=Pin(PIN_OLED_SDA), scl=Pin(PIN_OLED_SCL))
display = ssd1306.SSD1306_I2C(64, 48, i2c)
Screen.start_screen( display, DISPLAY_NAME )
time.sleep(2)

# network
ip_address = IFCONFIG.get_address()
short_ip_address = ip_address.split( '.' )

# Server
time.sleep(2)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip_address, 80))
s.listen(1)


# measure
d = DHT11.load_sensor( PIN_TEMP )
count = 0

Screen.clear_screen( display, DISPLAY_NAME )
Screen.show_ip( display, short_ip_address[3] )

output_html = True

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    request = cl.recv(2048)
    parseRequest = request.decode('utf-8').split(' ')

    if parseRequest[0] == 'GET':
        params = parseRequest[1]
        if params == '/html':
            output_html = True

        if params == '/json':
            output_html = False

    # Response
    d.measure()
    time.sleep(2) # wait !
    Screen.clear_screen(display, DISPLAY_NAME)
    temp = d.temperature()
    hum = d.humidity()
    count = count + 1
    Screen.print_screen_dht11(display, temp, hum, short_ip_address[3], count)

    jsonObject = [
        { "name": "temp", "value": temp },
        { "name": "hum", "value": hum },
    ]

    if output_html:
        html = '';
        for data in jsonObject:
            html = html + '<div><label>{}</label><span class="class-{}">{}</span></div>\n'.format(data.get('name'),
                                                                                                  data.get('name'),
                                                                                                  data.get('value'))
        response = Server.template(DISPLAY_NAME) % html
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'.encode())
    else:
        response = json.dumps( jsonObject )
        cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n'.encode())

    cl.send(response.encode())
    cl.close()





