from machine import Pin, I2C
from uio import StringIO
import ssd1306
import sys;

import utime as time
from screen import Screen
from server import Server
from dht11 import DHT11
from ifconfig import IFCONFIG

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

# measure
d = DHT11.load_sensor( PIN_TEMP )
count = 0

Screen.clear_screen( display, DISPLAY_NAME )

while True:
    display.text(DISPLAY_NAME, 0, 0, 1)

    try:
        d.measure()

        temp = d.temperature()
        hum = d.humidity()

        count = count + 1

        Screen.print_screen_dht11( display, temp, hum, ip_address, count )

    except Exception as e:
        s = StringIO();
        sys.print_exception(e, s)
        s = s.getvalue();
        s = s.split('\n')
        line = s[1].split(',');
        line = line[1];
        error = s[2];
        err = error + line;
        print(err)
        # Todo print error on WS
        #with open('error.log', 'a') as f:
        #    f.write(err)

        Screen.clear_screen(display, DISPLAY_NAME)
        Screen.print_screen_error( display, 'ERR !!!' )

    time.sleep(2)
    Screen.clear_screen( display, DISPLAY_NAME )

    #Server.pin_status()