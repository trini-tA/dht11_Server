import dht
from machine import Pin

class DHT11:
    def load_sensor( PIN_TEMP ):
        sensor = dht.DHT11(Pin(PIN_TEMP, Pin.IN, Pin.PULL_UP))
        return sensor
