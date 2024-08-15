import network
import time
import keys
from libs.umqtt_simple import MQTTClient

MQTT_HOST = "io.adafruit.com"
username = keys.ADAFRUIT_AIO_USERNAME
password = keys.ADAFRUIT_AIO_KEY

# WiFi Connection
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(keys.WIFI_SSID, keys.WIFI_PASSWORD)

    while wlan.isconnected()==False: # While your not connected
        print('Waiting for connection...')
        print("WiFi status:", wlan.status())
        time.sleep(1)

    if wlan.isconnected():
        print('Connection established:', wlan.isconnected())
        wifiInfo = wlan.ifconfig()
        print('Network configuration:', wifiInfo)
        ip = wifiInfo[0]
        print('Server ip: ', ip)
        return ip
    else:
        print('Failed to connect to WiFi')
        return None
    
def client():
    # Enter a random ID for this MQTT Client
    # It needs to be globally unique across all of Adafruit IO.
    mqtt_client_id = '202407021243'
    try:
        # Initialize our MQTTClient and connect to the MQTT server
        mqtt_client = MQTTClient(
            client_id=mqtt_client_id,
            server=MQTT_HOST,
            user=username,
            password=password
        )
        print("MQTT client created successfully")
        return mqtt_client
    except Exception as e:
        print(f"Failed to create MQTT client: {e}")
        return None
