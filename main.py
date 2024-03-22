from machine import Pin
from umqtt.simple import MQTTClient

import urequests as requests
import machine
import dht
import time
import network


Trig = Pin(13, Pin.OUT, 0)
Echo = Pin(14, Pin.IN, 0)

distance = 0  
soundVelocity = 340  # Set the speed of sound.

WIFI_SSID = ''  
WIFI_PASS = ''
MQTT_TOPIC = 'channels/2452163/publish'
MQTT_HOST = 'mqtt3.thingspeak.com'
MQTT_PORT = 1883
MQTT_username = ''
MQTT_clientId = ''
MQTT_password = ''

DEFAULT_MESSAGE = {
    "status": "SolomiiaZ"
}


def getDistance():
    Trig.value(1)
    time.sleep_us(10)
    Trig.value(0)
    while not Echo.value():
        pass
    pingStart = time.ticks_us()
    while Echo.value():
        pass
    pingStop = time.ticks_us()
    pingTime = time.ticks_diff(pingStop, pingStart) // 2
    distance = int(soundVelocity * pingTime // 10000)
    return distance

try:
    # WiFi connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        wlan.disconnect()
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        print("Trying to connect your WIFI")
    print("Connected!")
    
    # MQTT connection
    client = MQTTClient(client_id=MQTT_clientId, server=MQTT_HOST, port=MQTT_PORT, user=MQTT_username, password=MQTT_password)

    def settimeout(duration):
        pass

    client.settimeout = settimeout
    client.connect()
    
    while True:
        distance = getDistance()
        client.publish(MQTT_TOPIC, f"field4={distance}")
        time.sleep(2)

except Exception as error:
    raise error
